resource "aws_lambda_function" "transform_lambda" {
  function_name = "transform_lambda"
  image_uri = "${var.repository_url}:transform-latest"
  package_type = "Image"

  role = aws_iam_role.transform_lambda_exec_role.arn
  timeout = 300
  memory_size = 1024
}

resource "aws_s3_bucket_notification" "s3_trigger_for_transform_lambda" {
  bucket = "ingestion-bucket-st-trading-strategy-data-collection-pipeline"

  lambda_function {
    lambda_function_arn = aws_lambda_function.transform_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_lambda_permission.allow_s3_to_invoke_transform_lambda
  ]
}

resource "aws_lambda_permission" "allow_s3_to_invoke_transform_lambda" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.transform_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::ingestion-bucket-st-trading-strategy-data-collection-pipeline"
}