variable "aws_region" {
  description = "Région AWS"
  type        = string
  default     = "eu-west-3"
}

variable "environment" {
  description = "Environnement"
  type        = string
  default     = "dev"
}

variable "bucket_name" {
  description = "Nom du bucket S3"
  type        = string
  default     = "datasai-storage-2026"
}

variable "ami_id" {
  description = "AMI Amazon Linux 2023"
  type        = string
  default     = "ami-0302f42a44bf53a45"
}

variable "instance_type" {
  description = "Type EC2"
  type        = string
  default     = "t3.micro"
}

variable "aws_access_key" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
}

variable "aws_secret_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}