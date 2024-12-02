//========================================================================================
//=================================== API Gateway ========================================
//========================================================================================

resource "aws_api_gateway_rest_api" "prod_api" {
  name        = "prod_api"
  description = "Production API"

}

resource "aws_api_gateway_resource" "all" {
  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  parent_id   = aws_api_gateway_rest_api.prod_api.root_resource_id
  path_part   = "all"

}

resource "aws_api_gateway_resource" "departments" {
  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  parent_id   = aws_api_gateway_rest_api.prod_api.root_resource_id
  path_part   = "departments"

}

resource "aws_api_gateway_resource" "departments_id" {
  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  parent_id   = aws_api_gateway_resource.departments.id
  path_part   = "{id}"

}

resource "aws_api_gateway_resource" "locations" {
  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  parent_id   = aws_api_gateway_rest_api.prod_api.root_resource_id
  path_part   = "locations"

}


resource "aws_api_gateway_resource" "locations_id" {
  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  parent_id   = aws_api_gateway_resource.locations.id
  path_part   = "{id}"
}

resource "aws_api_gateway_resource" "personnel" {
  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  parent_id   = aws_api_gateway_rest_api.prod_api.root_resource_id
  path_part   = "personnel"
}

resource "aws_api_gateway_resource" "personnel_id" {
  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  parent_id   = aws_api_gateway_resource.personnel.id
  path_part   = "{id}"
}

resource "aws_api_gateway_method" "all_get" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.all.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "all_options" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.all.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "departments_get" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.departments.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "departments_options" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.departments.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "departments_post" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.departments.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "departments_id_delete" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.departments_id.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "departments_id_get" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.departments_id.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "locations_get" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.locations.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "locations_options" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.locations.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "locations_post" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.locations.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "locations_id_delete" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.locations_id.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "personnel_get" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.personnel.id
  http_method   = "GET"
  authorization = "NONE"

}

resource "aws_api_gateway_method" "personnel_options" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.personnel.id
  http_method   = "OPTIONS"
  authorization = "NONE"

}

resource "aws_api_gateway_method" "personnel_post" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.personnel.id
  http_method   = "POST"
  authorization = "NONE"

}

resource "aws_api_gateway_method" "personnel_id_delete" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.personnel_id.id
  http_method   = "DELETE"
  authorization = "NONE"

}

resource "aws_api_gateway_method" "personnel_id_get" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.personnel_id.id
  http_method   = "GET"
  authorization = "NONE"

}

resource "aws_api_gateway_method" "personnel_id_put" {
  rest_api_id   = aws_api_gateway_rest_api.prod_api.id
  resource_id   = aws_api_gateway_resource.personnel_id.id
  http_method   = "PUT"
  authorization = "NONE"

}

// Defining Lambda integration for each method
resource "aws_api_gateway_integration" "lambda_integration" {
  for_each = {
    "all_get" = aws_api_gateway_method.all_get
    "departments_get" = aws_api_gateway_method.departments_get
    "departments_post" = aws_api_gateway_method.departments_post
    "departments_id_delete" = aws_api_gateway_method.departments_id_delete
    "departments_id_get" = aws_api_gateway_method.departments_id_get
    "locations_get" = aws_api_gateway_method.locations_get
    "locations_post" = aws_api_gateway_method.locations_post
    "locations_id_delete" = aws_api_gateway_method.locations_id_delete
    "personnel_get" = aws_api_gateway_method.personnel_get
    "personnel_post" = aws_api_gateway_method.personnel_post
    "personnel_id_delete" = aws_api_gateway_method.personnel_id_delete
    "personnel_id_get" = aws_api_gateway_method.personnel_id_get
    "personnel_id_put" = aws_api_gateway_method.personnel_id_put
  }

  rest_api_id             = aws_api_gateway_rest_api.prod_api.id
  resource_id             = each.value.resource_id
  http_method             = each.value.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:eu-west-2:lambda:path/2015-03-31/functions/${aws_lambda_function.my_lambda.arn}/invocations"

}

# Options method integration
resource "aws_api_gateway_integration" "options_integration" {
  for_each = {
    "all_options" = aws_api_gateway_method.all_options
    "departments_options" = aws_api_gateway_method.departments_options
    "locations_options" = aws_api_gateway_method.locations_options
    "personnel_options" = aws_api_gateway_method.personnel_options
  }

  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }

}

# Method responses for non-OPTIONS methods
resource "aws_api_gateway_method_response" "lambda_method_response" {
  for_each = aws_api_gateway_integration.lambda_integration

  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }

}

# Method responses for OPTIONS methods
resource "aws_api_gateway_method_response" "options_method_response" {
  for_each = aws_api_gateway_integration.options_integration

  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = "200"

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin" = true
  }

}

# Integration responses for OPTIONS methods
resource "aws_api_gateway_integration_response" "options_integration_response" {
  for_each = aws_api_gateway_integration.options_integration

  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  resource_id = each.value.resource_id
  http_method = each.value.http_method
  status_code = aws_api_gateway_method_response.options_method_response[each.key].status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT,DELETE'",
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }

  depends_on = [aws_api_gateway_integration.options_integration]
}

# Deploy the API
resource "aws_api_gateway_deployment" "prod_deployment" {
  rest_api_id = aws_api_gateway_rest_api.prod_api.id
  stage_name  = "prod"
  triggers = {
    redeployment = sha1(jsonencode([
      aws_lambda_function.my_lambda,
      aws_api_gateway_integration.lambda_integration,
      aws_api_gateway_integration.options_integration
    ]))
  }
  depends_on = [
    aws_lambda_function.my_lambda,
    aws_lambda_permission.api_gateway,
    aws_api_gateway_integration.lambda_integration,
    aws_api_gateway_integration.options_integration,
    aws_api_gateway_integration_response.options_integration_response,
    aws_api_gateway_method_response.lambda_method_response,
    aws_api_gateway_method_response.options_method_response
  ]
}

# Output the invoke URL.
output "invoke_url" {
  value = aws_api_gateway_deployment.prod_deployment.invoke_url
}