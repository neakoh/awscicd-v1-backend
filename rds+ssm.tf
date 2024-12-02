#==========================================================================================
#-----------------------------------------RDS----------------------------------------------
#==========================================================================================
// RDS Definition
resource "aws_db_instance" "my_rds" {
  identifier         = "my-rds-instance"
  engine             = "mysql"  
  engine_version     = "8.0"   
  instance_class     = "db.t3.micro"  
  allocated_storage   = 20  
  db_subnet_group_name = aws_db_subnet_group.my_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  username           = "my_username" 
  password           = "yourpassword"
  skip_final_snapshot = true

  storage_encrypted = true

  tags = {
    Name = "my-rds-instance"
  }
}
# RDS placement within VPC.
resource "aws_db_subnet_group" "my_db_subnet_group" {
  name       = "my-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id 

  tags = {
    Name = "my-db-subnet-group"
  }
}

#==========================================================================================
#-----------------------------------------SSM----------------------------------------------
#==========================================================================================
// Creating new secret
resource "random_string" "rds_suffix" {
  length  = 8
  special = false
}

resource "aws_secretsmanager_secret" "rds_secret" {
  name        = "rds-credentials-${random_string.rds_suffix.result}"
  description = "RDS credentials for my database"

  tags = {
    Name = "rds-credentials"
  }

}
// Setting new secret values
resource "aws_secretsmanager_secret_version" "rds_secret_version" {
  secret_id     = aws_secretsmanager_secret.rds_secret.id
  secret_string = jsonencode({
    username = aws_db_instance.my_rds.username
    password = aws_db_instance.my_rds.password
  })
}

#==========================================================================================
#---------------------------------------Outputs--------------------------------------------
#==========================================================================================

output "rds_name" {
  description = "RDS database name."
  value       = aws_db_instance.my_rds.identifier
}

output "rds_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = aws_db_instance.my_rds.endpoint
}

output "secret_name" {
  description = "The endpoint of the RDS instance"
  value       = aws_secretsmanager_secret.rds_secret.name
}