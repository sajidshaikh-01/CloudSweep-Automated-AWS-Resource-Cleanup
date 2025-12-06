###############################################
# SNS TOPIC FOR NOTIFICATIONS
###############################################
resource "aws_sns_topic" "cronda_topic" {
  name = "CrondaNotifications"
}

###############################################
# LAMBDA FUNCTION
###############################################
resource "aws_lambda_function" "cronda_lambda" {
  function_name = "CrondaLambda"

  role    = aws_iam_role.cronda_lambda_role.arn
  handler = "cronda.lambda_handler"
  runtime = "python3.10"

  filename         = "${path.module}/../cronda.zip"
  source_code_hash = filebase64sha256("${path.module}/../cronda.zip")

  timeout     = 900 # Max allowed (15 min)
  memory_size = 512

  environment {
    variables = {
      THRESHOLD_HOURS = "3"
      DRY_RUN         = "true"
      SNS_TOPIC_ARN   = aws_sns_topic.cronda_topic.arn
    }
  }
}

###############################################
# PERMISSION: ALLOW EVENTBRIDGE TO TRIGGER LAMBDA
###############################################
resource "aws_lambda_permission" "allow_event" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cronda_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cronda_schedule.arn
}

###############################################
# EVENTBRIDGE RULE (CRON JOB)
###############################################
resource "aws_cloudwatch_event_rule" "cronda_schedule" {
  name                = "CrondaScheduler"
  description         = "Run Cronda every 30 minutes"
  schedule_expression = "rate(30 minutes)"
}

resource "aws_cloudwatch_event_target" "cronda_target" {
  rule      = aws_cloudwatch_event_rule.cronda_schedule.name
  target_id = "CrondaLambdaTarget"
  arn       = aws_lambda_function.cronda_lambda.arn
}
