resource "aws_lambda_function" "load_lambda" {
  function_name = "load_lambda"
  image_uri = "${var.repository_url}:load-latest"
  package_type = "Image"

  role = aws_iam_role.load_lambda_exec_role.arn
  timeout = 300
  memory_size = 1024
}

resource "aws_s3_bucket_notification" "s3_trigger_for_load_lambda" {
  bucket = "processed-bucket-st-trading-strategy-data-collection-pipeline"

  lambda_function {
    lambda_function_arn = aws_lambda_function.load_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_lambda_permission.allow_s3_to_invoke_load_lambda
  ]
}

resource "aws_lambda_permission" "allow_s3_to_invoke_load_lambda" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.load_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::processed-bucket-st-trading-strategy-data-collection-pipeline"
}