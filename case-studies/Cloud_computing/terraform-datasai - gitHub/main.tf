# Bloc terraform — version et providers
terraform {
  required_version = ">= 1.2"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key

  default_tags {
    tags = {
      ManagedBy   = "Terraform"
      Project     = "DataSAI"
      Environment = var.environment
    }
  }
}

# Ressource 1
resource "aws_s3_bucket" "datasai_bucket" {
  bucket = var.bucket_name

  tags = {
    Name = "DataSAI Storage Bucket"
  }
}

# Ressource 2 
resource "aws_s3_bucket_public_access_block" "datasai_bucket_block" {
  bucket = aws_s3_bucket.datasai_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Ressource 3
resource "aws_instance" "datasai_server" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = "DataSAI Server"
  }
}