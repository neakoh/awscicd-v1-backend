#==========================================================================================
#------------------------------------Security Groups---------------------------------------
#==========================================================================================
// Lambda security groups
resource "aws_security_group" "lambda_sg" {
  name        = "lambda-sg"
  description = "Security group for Lambda functions"
  vpc_id      = aws_vpc.main.id 

  // Outbound traffic to Secrets Manager
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  // Outbound to RDS
  egress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  tags = {
    Name = "lambda-sg"
  }
}

// Containers
resource "aws_security_group" "containers_sg" {
  name        = "containers-sg"
  description = "Security group for containers"
  vpc_id      = aws_vpc.main.id 

  tags = {
    Name = "containers-sg"
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }
}

// Security Group for ALB
resource "aws_security_group" "alb_sg" {
  name        = "alb-sg"
  description = "Security group for ALB"
  vpc_id      = aws_vpc.main.id 

  // Allowing inbound traffic from the internet
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["86.142.89.147/32"] 
  }

  tags = {
    Name = "alb-sg"
  }
}

// SSM Interface Endpoint
resource "aws_security_group" "secretsmanager_endpoint_sg" {
  name        = "secretsmanager-endpoint-sg"
  description = "Security group for Secrets Manager Interface Endpoint"
  vpc_id      = aws_vpc.main.id 

  tags = {
    Name = "secretsmanager-endpoint-sg"
  }
}

// RDS
resource "aws_security_group" "rds_sg" {
  name        = "rds-sg"
  description = "Security group for RDS"
  vpc_id      = aws_vpc.main.id 

  tags = {
    Name = "rds-sg"
  }
}

// Allowing traffic from ALB to containers over HTTP
resource "aws_security_group_rule" "alb_to_containers_ingress_http" {
  type                     = "ingress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  security_group_id        = aws_security_group.containers_sg.id
  source_security_group_id = aws_security_group.alb_sg.id
}
resource "aws_security_group_rule" "alb_to_containers_egress_http" {
  type                     = "egress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  security_group_id        = aws_security_group.alb_sg.id
  source_security_group_id = aws_security_group.containers_sg.id
}

// Allow Lambda to access Secrets Manager over HTTPS
resource "aws_security_group_rule" "lambda_to_secretsmanager" {
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.secretsmanager_endpoint_sg.id
  source_security_group_id = aws_security_group.lambda_sg.id
}

// Allow Lambda to access RDS over MySQL (3306)
resource "aws_security_group_rule" "lambda_to_rds" {
  type                     = "ingress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds_sg.id
  source_security_group_id = aws_security_group.lambda_sg.id
}

#==========================================================================================
#-----------------------------------------Outputs------------------------------------------
#==========================================================================================
output "alb-sg-id" {
  description = "alb sg id"
  value       = aws_security_group.alb_sg.id
}

output "container-sg-id" {
  description = "container sg id"
  value       = aws_security_group.containers_sg.id
}