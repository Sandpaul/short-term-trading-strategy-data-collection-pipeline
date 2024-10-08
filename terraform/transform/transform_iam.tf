resource "aws_iam_role" "transform_lambda_exec_role" {
  name = "transform_lambda_exec_role"
  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "transform_lambda_s3_policy" {
  name = "transform_lambda_s3_policy"
  description = "IAM policy for transform Lambda to access S3"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject"
        ],
        "Resource": "arn:aws:s3:::ingestion-bucket-st-trading-strategy-data-collection-pipeline/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "transform_lambda_s3_policy_attach" {
  role = aws_iam_role.transform_lambda_exec_role.name
  policy_arn = aws_iam_policy.transform_lambda_s3_policy.arn
}

resource "aws_iam_policy" "transform_lambda_ecr_policy" {
  name = "transform_lambda_ecr_policy"
  description = "IAM policy for transform Lambda to access ECR"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken"
        ],
        "Resource": "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "transform_lambda_ecr_policy_attach" {
  role = aws_iam_role.transform_lambda_exec_role.name
  policy_arn = aws_iam_policy.transform_lambda_ecr_policy.arn
}