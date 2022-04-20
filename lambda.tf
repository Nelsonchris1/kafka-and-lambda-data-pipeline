locals {
    lambda-zip-location = "outputs/welcome.zip"
}

data "archive_file" "init" {
  type        = "zip"
  source_file = "welcome.py"
  output_path = local.lambda-zip-location
}

resource "aws_lambda_function" "test_lambda" {
  # If the file is not in the current working directory you will need to include a 
  # path.module in the filename.
  filename      = local.lambda-zip-location
  function_name = "welcome"
  role          = aws_iam_role.lambda_role.arn
  handler       = "welcome.hello" 

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  #source_code_hash = filebase64sha256(local.lambda-zip-location)

  runtime = "python3.9"
}

resource "aws_cloudwatch_event_rule" "customer-trigger" {
    name = "customer-trigger"
    description = "Fires every five minutes"
    event_pattern  = <<EOF
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["customer-practice"]
    }
  }
}
EOF
}

resource "aws_cloudwatch_event_target" "customer-trigger-target"{
    rule = "${aws_cloudwatch_event_rule.customer-trigger.name}"
    target_id = "test_lambda"
    arn = "${aws_lambda_function.test_lambda.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_test_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.test_lambda.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.customer-trigger.arn}"
}

# # Lambda layer
# resource "aws_lambda_layer_version" "lambda_layer" {
#   filename   = "page-view.zip"
#   layer_name = "page-view-layer"

#   compatible_runtimes = ["python3.9"]
# }