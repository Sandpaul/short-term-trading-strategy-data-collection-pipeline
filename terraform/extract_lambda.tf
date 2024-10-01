resource "aws_lambda_function" "extract_lambda" {
  function_name = "extract_lambda"
  s3_bucket = aws_s3_bucket.lambda_bucket.bucket
  s3_key = "extract_lambda_package.zip"
  handler = "src.extract.extract_and_save_data.lambda_handler"
  runtime = "python3.12.5"

  role = aws_iam_role.extract_lambda_exec_role.arn

  environment {
    variables = {
      BUCKET_NAME = "ingestion-bucket-st-trading-strategy-data-collection-pipeline"
    }
  }
}

resource "aws_cloudwatch_event_rule" "extract_daily_trigger" {
  name = "daily_lambda_trigger"
  description = "Triggers the extract Lambda function daily"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "extract_lambda_trigger" {
  rule = aws_cloudwatch_event_rule.extract_daily_trigger.name
  target_id = "extract_lambda"
  arn = aws_lambda_function.extract_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_invoke_extract_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.extract_lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.extract_daily_trigger.arn
}