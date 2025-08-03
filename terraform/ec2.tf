# Security Group
resource "aws_security_group" "allow_ssh_8080_8000" {
name        = "allow-ssh-8080-8000"
description = "Allow SSH, 8080, and 8000 inbound traffic"

ingress {
  description = "SSH"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

ingress {
  description = "Port 8080"
  from_port   = 8080
  to_port     = 8080
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

ingress {
  description = "Port 8000"
  from_port   = 8000
  to_port     = 8000
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

egress {
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}
}

# Get Amazon Linux 2 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.7.20250623.1-kernel-6.1-x86_64"]
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.allow_ssh_8080_8000.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y git ansible
              EOF

  tags = {
    Name = "MyTerraformEC2"
  }
}
