resource "random_id" "bucket_suffix" {
  byte_length = 6
}

resource "aws_s3_bucket" "landing_bucket" {
  bucket = "landing-bucket-${random_id.bucket_suffix.hex}"
  tags = local.common_tags
}

resource "aws_iam_policy" "s3_access_policy" {
  name = "ecsTaskS3AccessPolicy"

  policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect   : "Allow",
        Action   : ["s3:PutObject", "s3:GetObject"],
        Resource : [
          "${aws_s3_bucket.landing_bucket.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_s3_access" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

output "bucket_name" {
  value = aws_s3_bucket.landing_bucket.bucket
}