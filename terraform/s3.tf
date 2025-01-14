resource "random_id" "bucket_suffix" {
  byte_length = 6
}

resource "aws_s3_bucket" "landing_bucket" {
  bucket = "landing-bucket-${random_id.bucket_suffix.hex}"
}

output "bucket_name" {
  value = aws_s3_bucket.landing_bucket.bucket
}