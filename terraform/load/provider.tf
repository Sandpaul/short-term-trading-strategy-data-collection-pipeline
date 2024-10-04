provider "aws" {
    region = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket = "terraform-state-bucket-trading-data-collection-pipeline"
    key = "load/terraform.tfstate"
    region = "eu-west-2"
    dynamodb_table = "lock-table-st-trading-data-collection-pipeline"
    encrypt = true
  }
  
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "5.7.0"
    }
  }
}