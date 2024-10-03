resource "aws_cloudwatch_log_group" "transform_lambda_log_group" {
  name = "/aws/lambda/${aws_lambda_function.transform_lambda.function_name}"
  retention_in_days = 14
}

resource "aws_iam_role_policy_attachment" "transform_logging" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role = aws_iam_role.transform_lambda_exec_role.name
}