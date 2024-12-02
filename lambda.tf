#==========================================================================================
#----------------------------------------Lambda--------------------------------------------
#==========================================================================================
// Defining Lambda role and permissions
resource "aws_iam_role" "lambda_role" {
  name = "lambda-vpc-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda-vpc-api-policy"
  description = "Policy for Lambda to access RDS, Secrets Manager, EC2, and API Gateway"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "rds-db:connect",
          "rds:DescribeDBInstances",
          "rds:DescribeDBClusters"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface",
          "ec2:AssignPrivateIpAddresses",
          "ec2:UnassignPrivateIpAddresses"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "execute-api:Invoke",
          "execute-api:ManageConnections"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

// Lambda function
resource "aws_lambda_function" "my_lambda" {
  function_name = "get_company_records_function"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9" 
  timeout       = 10

  s3_bucket = "cicd-project-lambda"
  s3_key    = "get-company-records-lambda.zip"

  // Placing Lambda inside private subnets so that it can communicate with RDS
  vpc_config {
    subnet_ids         = [aws_subnet.private[0].id, aws_subnet.private[1].id]
    security_group_ids = [aws_security_group.lambda_sg.id] 
  }

}

// Linking each API method
resource "aws_lambda_permission" "api_gateway" {
  for_each = {
    "all_get" = { method = aws_api_gateway_method.all_get, path = "all" }
    "departments_get" = { method = aws_api_gateway_method.departments_get, path = "departments" }
    "departments_post" = { method = aws_api_gateway_method.departments_post, path = "departments" }
    "departments_id_delete" = { method = aws_api_gateway_method.departments_id_delete, path = "departments/{id}" }
    "departments_id_get" = { method = aws_api_gateway_method.departments_id_get, path = "departments/{id}" }
    "locations_get" = { method = aws_api_gateway_method.locations_get, path = "locations" }
    "locations_post" = { method = aws_api_gateway_method.locations_post, path = "locations" }
    "locations_id_delete" = { method = aws_api_gateway_method.locations_id_delete, path = "locations/{id}" }
    "personnel_get" = { method = aws_api_gateway_method.personnel_get, path = "personnel" }
    "personnel_post" = { method = aws_api_gateway_method.personnel_post, path = "personnel" }
    "personnel_id_delete" = { method = aws_api_gateway_method.personnel_id_delete, path = "personnel/{id}" }
    "personnel_id_get" = { method = aws_api_gateway_method.personnel_id_get, path = "personnel/{id}" }
    "personnel_id_put" = { method = aws_api_gateway_method.personnel_id_put, path = "personnel/{id}" }
  }

  statement_id  = "AllowAPIGatewayInvoke_${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn    = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.prod_api.id}/*/${each.value.method.http_method}/${each.value.path}"

}

data "aws_caller_identity" "current" {}