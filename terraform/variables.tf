variable "aws_region" {
  description = "AWS region"
  default     = "eu-central-1"
}

variable "ami_id" {
  description = "Amazon Linux 2023 AMI ID for eu-central-1"
  default     = "ami-0ae2eb6210612f5a0"
}

variable "jenkins_instance_type" {
  description = "Instance type for Jenkins VM"
  default     = "t3.small"
}

variable "staging_instance_type" {
  description = "Instance type for Staging VM"
  default     = "t3.small"
}

variable "production_instance_type" {
  description = "Instance type for Production VM"
  default     = "t3.small"
}

variable "key_name" {
  description = "Name of the SSH key pair in AWS"
  default     = "car-inventory-key"
}

variable "my_ip" {
  description = "Your home IP address for SSH access"
  default     = "82.78.233.3/32"
}

variable "github_repo" {
  description = "GitHub repository URL"
  default     = "https://github.com/prafalex/car-inventory-devops.git"
}