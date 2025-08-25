variable "region" {
  description = "AWS region to deploy resources"
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.small"
}

variable "key_name" {
  description = "EC2 instance key pair"
  type        = string
}

variable "aws_profile" {
  default     = "3tierdemo"
}