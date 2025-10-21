# deployment/main.tf

provider "aws" {
  region = "us-east-1" # Or your preferred region
}

resource "aws_iam_role" "vanguard_agent_lambda_role" {
  name = "VanguardAgentLambdaRole"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.vanguard_agent_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "../log_analyzer.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "vanguard_agent" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "VanguardAgent"
  role          = aws_iam_role.vanguard_agent_lambda_role.arn
  handler       = "log_analyzer.lambda_handler"
  runtime       = "python3.9"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      PRAETORIUM_NEXUS_API_URL = "https://your-praetorium-nexus-api-endpoint.com/api"
      # In a real deployment, these would be KMS-encrypted or stored in Secrets Manager
      PRAETORIUM_NEXUS_API_KEY = "your_secure_api_key_here"
      LLM_SERVICE_API_KEY      = "your_secure_llm_api_key_here"
    }
  }

  tags = {
    Project = "VanguardAgent"
    GRC     = "Threat-Informed"
  }
}
