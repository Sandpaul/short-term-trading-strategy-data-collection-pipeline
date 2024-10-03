resource "aws_lambda_function" "transform_lambda" {
  function_name = "transform_lambda"
  image_uri = "${aws_ecr_repository.container_repo.repository_url}:transform-latest"
  package_type = "Image"

  role = aws_iam_role.transform_lambda_exec_role.arn
  timeout = 300
  memory_size = 1024
}

resource "aws_s3_bucket_notification" "transform_lambda_trigger" {
  bucket = aws_s3_bucket.ingestion_bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.transform_lambda.arn
    events = ["s3:ObjectCreated:*"]
  }
}

resource "aws_lambda_permission" "allow_s3_transform" {
  action = "lambda:InvokeFunction"
  function_name = "transform_lambda"
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.ingestion_bucket.arn
  source_account = data.aws_caller_identity.current.account_id
}