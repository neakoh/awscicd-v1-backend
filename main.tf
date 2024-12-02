#==========================================================================================
#------------------------------------General Config----------------------------------------
#==========================================================================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"  # Adjust the version as needed
    }
  }

  backend "remote" {
    organization = "neakoh-org"

    workspaces {
      name = "gitlab-project-terraform" 
    }
  }
}
provider "aws" {
  region = "eu-west-2" 
}
 
#==========================================================================================
#-----------------------------------------VPC----------------------------------------------
#==========================================================================================

data "aws_availability_zones" "available" {
  state = "available"
}
data "aws_region" "current"{
  name = "eu-west-2"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "my_company_database"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

// Subnets
resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index * 2}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index * 2 + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-subnet-${count.index + 1}"
  }
}

// Route Table
// Defining public route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "public-route-table"
  }
}
// Defining private route tables
resource "aws_route_table" "private" {
  count  = 2
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "private-route-table-${count.index + 1}"
  }
}

// Linking public subs to public route table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

// Private subs to respective route tables
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

// VPC endpoint to ensure Lambda can communicate with Secrets Manager.
resource "aws_vpc_endpoint" "secretsmanager" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${data.aws_region.current.name}.secretsmanager"
  vpc_endpoint_type   = "Interface"
  private_dns_enabled = true

  subnet_ids = aws_subnet.private[*].id

  security_group_ids = [
    aws_security_group.secretsmanager_endpoint_sg.id
  ]

  tags = {
    Name = "secretsmanager-endpoint"
  }
}

#==========================================================================================
#-----------------------------------------Outputs------------------------------------------
#==========================================================================================

// All outputs passed to repo 2 
output "public_subnet_ids" {
  description = "pubsub ids"
  value = aws_subnet.public[*].id 
}

output "vpc_id" {
  description = "pubsub ids"
  value = aws_vpc.main.id  
}