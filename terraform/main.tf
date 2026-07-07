terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "terraform"
}

resource "aws_security_group" "car_inventory_sg" {
  name        = "car-inventory-sg"
  description = "car inventory project security group"

  # SSH access restricted to my IP only
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  # Jenkins needs to be reachable from anywhere for GitHub webhooks
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # staging uses 3001/8001, blue uses 3002/8002, green uses 3003/8003
  ingress {
    from_port   = 3001
    to_port     = 3003
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8001
    to_port     = 8003
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # allow SSH between VMs within the same VPC
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["172.31.0.0/16"]
    }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "car-inventory-sg"
    Project = "car-inventory-devops"
  }
}

# Jenkins runs as a Docker container on this VM
# The Docker socket is mounted so Jenkins can spin up app containers directly
# infra-state is mounted so the nginx config persists across Jenkins workspace cleanups
resource "aws_instance" "jenkins" {
  ami                    = var.ami_id
  instance_type          = var.jenkins_instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.car_inventory_sg.id]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  user_data = <<-EOF
    #!/bin/bash
    set -e
    exec > /var/log/user-data.log 2>&1

    dnf update -y
    dnf install -y docker git
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ec2-user

    mkdir -p /usr/local/lib/docker/cli-plugins
    curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
      -o /usr/local/lib/docker/cli-plugins/docker-compose
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

    dd if=/dev/zero of=/swapfile bs=1M count=2048
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile swap swap defaults 0 0' >> /etc/fstab

    docker network create devops-net || true
    mkdir -p /home/ec2-user/infra-state
    chown ec2-user:ec2-user /home/ec2-user/infra-state

    docker run -d \
      --name jenkins \
      --network devops-net \
      -p 8080:8080 \
      -p 50000:50000 \
      -v jenkins_home:/var/jenkins_home \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v /home/ec2-user/infra-state:/home/ec2-user/infra-state \
      --restart unless-stopped \
      jenkins/jenkins:lts

    # wait for Jenkins to start before running exec commands
    sleep 120

    # the docker group GID inside the Jenkins container won't match the host socket GID
    # by default — this causes permission denied when Jenkins tries to run docker commands.
    # we fix it by reading the actual GID from the socket and aligning the group inside.
    DOCKER_GID=$$(stat -c '%g' /var/run/docker.sock)
    docker exec -u root jenkins bash -c "
      apt-get update -qq > /dev/null &&
      apt-get install -y -qq docker.io python3-venv nodejs npm curl > /dev/null &&
      groupadd -g $${DOCKER_GID} docker 2>/dev/null || groupmod -g $${DOCKER_GID} docker &&
      usermod -aG docker jenkins &&
      mkdir -p /usr/local/lib/docker/cli-plugins &&
      curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
        -o /usr/local/lib/docker/cli-plugins/docker-compose > /dev/null &&
      chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
    "

    docker restart jenkins
    echo "done" > /home/ec2-user/infra-state/.setup-complete
  EOF

  tags = {
    Name    = "car-inventory-jenkins"
    Role    = "jenkins"
    Project = "car-inventory-devops"
  }
}

# staging is a clean VM that receives deployments from Jenkins
# Jenkins SSHes in (or uses docker exec remotely) to run docker compose up
resource "aws_instance" "staging" {
  ami                    = var.ami_id
  instance_type          = var.staging_instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.car_inventory_sg.id]

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  user_data = <<-EOF
    #!/bin/bash
    set -e
    exec > /var/log/user-data.log 2>&1

    dnf update -y
    dnf install -y docker git
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ec2-user

    mkdir -p /usr/local/lib/docker/cli-plugins
    curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
      -o /usr/local/lib/docker/cli-plugins/docker-compose
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

    dd if=/dev/zero of=/swapfile bs=1M count=2048
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile swap swap defaults 0 0' >> /etc/fstab

    cd /home/ec2-user
    git clone ${var.github_repo} car-inventory-devops
    chown -R ec2-user:ec2-user car-inventory-devops

    echo "done" > /home/ec2-user/.setup-complete
  EOF

  tags = {
    Name    = "car-inventory-staging"
    Role    = "staging"
    Project = "car-inventory-devops"
  }
}

# production runs the shared postgres database plus blue and green environments
# nginx-prod.conf is seeded here from the repo and then owned by Jenkins going forward —
# each deployment rewrites it in place to record which environment is currently live
resource "aws_instance" "production" {
  ami                    = var.ami_id
  instance_type          = var.production_instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.car_inventory_sg.id]

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  user_data = <<-EOF
    #!/bin/bash
    set -e
    exec > /var/log/user-data.log 2>&1

    dnf update -y
    dnf install -y docker git
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ec2-user

    mkdir -p /usr/local/lib/docker/cli-plugins
    curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
      -o /usr/local/lib/docker/cli-plugins/docker-compose
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

    dd if=/dev/zero of=/swapfile bs=1M count=2048
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile swap swap defaults 0 0' >> /etc/fstab

    docker network create car-production-network || true

    mkdir -p /home/ec2-user/infra-state
    mkdir -p /home/ec2-user/db-backups
    chown ec2-user:ec2-user /home/ec2-user/infra-state
    chown ec2-user:ec2-user /home/ec2-user/db-backups

    cd /home/ec2-user
    git clone ${var.github_repo} car-inventory-devops
    chown -R ec2-user:ec2-user car-inventory-devops

    # seed the persistent nginx config from the repo
    # after this point Jenkins owns it — never touched by git again
    cp /home/ec2-user/car-inventory-devops/infra/nginx/nginx-prod.conf \
       /home/ec2-user/infra-state/nginx-prod.conf

    echo "done" > /home/ec2-user/.setup-complete
  EOF

  tags = {
    Name    = "car-inventory-production"
    Role    = "production"
    Project = "car-inventory-devops"
  }
}

resource "aws_eip" "jenkins_eip" {
  instance = aws_instance.jenkins.id
  domain   = "vpc"
  tags = {
    Name    = "car-inventory-jenkins-eip"
    Project = "car-inventory-devops"
  }
}

resource "aws_eip" "staging_eip" {
  instance = aws_instance.staging.id
  domain   = "vpc"
  tags = {
    Name    = "car-inventory-staging-eip"
    Project = "car-inventory-devops"
  }
}

resource "aws_eip" "production_eip" {
  instance = aws_instance.production.id
  domain   = "vpc"
  tags = {
    Name    = "car-inventory-production-eip"
    Project = "car-inventory-devops"
  }
}