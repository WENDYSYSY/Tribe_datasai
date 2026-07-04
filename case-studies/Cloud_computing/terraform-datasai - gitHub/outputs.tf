output "bucket_arn" {
  value = aws_s3_bucket.datasai_bucket.arn
}

output "instance_public_ip" {
  value = aws_instance.datasai_server.public_ip
}