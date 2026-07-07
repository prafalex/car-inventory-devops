output "jenkins_url" {
  value = "http://${aws_eip.jenkins_eip.public_ip}:8080"
}

output "jenkins_ssh" {
  value = "ssh -i car-inventory-key.pem ec2-user@${aws_eip.jenkins_eip.public_ip}"
}

output "staging_ssh" {
  value = "ssh -i car-inventory-key.pem ec2-user@${aws_eip.staging_eip.public_ip}"
}

output "production_ssh" {
  value = "ssh -i car-inventory-key.pem ec2-user@${aws_eip.production_eip.public_ip}"
}

output "staging_frontend" {
  value = "http://${aws_eip.staging_eip.public_ip}:3001"
}

output "production_blue" {
  value = "http://${aws_eip.production_eip.public_ip}:3002"
}

output "production_green" {
  value = "http://${aws_eip.production_eip.public_ip}:3003"
}

output "staging_private_ip" {
  value = "172.31.45.138"
}

output "production_private_ip" {
  value = "172.31.36.139"
}