resource "aws_iam_role" "extract_lambda_exec_role" {
    name = "extract_lambda_exec_role"
    assume_role_policy = jsonencode({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_iam_policy" "extract_lambda_s3_policy" {
  name = "lambda_s3_policy"
  description = "IAM policy for extract Lambda to access s3"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:s3:::ingestion-bucket-st-trading-strategy-data-collection-pipeline/*"
        }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "extract_lambda_s3_policy_attach" {
  role = aws_iam_role.extract_lambda_exec_role.name
  policy_arn = aws_iam_policy.extract_lambda_s3_policy.arn
}