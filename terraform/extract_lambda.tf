resource "aws_lambda_function" "extract_lambda" {
  function_name = "extract_lambda"
  image_uri = "${aws_ecr_repository.container_repo.repository_url}:extract-latest"
  package_type = "Image"
  
  role = aws_iam_role.extract_lambda_exec_role.arn
  timeout = 300
}

resource "aws_cloudwatch_event_rule" "extract_daily_trigger" {
  name = "daily_lambda_trigger"
  description = "Triggers the extract Lambda function daily at midnight US Eastern Time"
  schedule_expression = "cron(0 5 * * ? *)"
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