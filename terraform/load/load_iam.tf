resource "aws_iam_role" "load_lambda_exec_role" {
  name = "load_lambda_exec_role"
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

resource "aws_iam_policy" "load_lambda_s3_policy" {
  name = "load_lambda_s3_policy"
  description = "IAM policy for load Lambda to access S3"
  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject"
        ],
        "Resource": "arn:aws:s3:::processed-bucket-st-trading-strategy-data-collection-pipeline/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "load_lambda_s3_policy_attach" {
  role = aws_iam_role.load_lambda_exec_role.name
  policy_arn = aws_iam_policy.load_lambda_s3_policy.arn
}

resource "aws_iam_policy" "load_lambda_ecr_policy" {
  name = "load_lambda_ecr_policy"
  description = "IAM policy for load Lambda to access ECR"

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

resource "aws_iam_role_policy_attachment" "load_lambda_ecr_policy_attach" {
  role = aws_iam_role.load_lambda_exec_role.name
  policy_arn = aws_iam_policy.load_lambda_ecr_policy.arn
}