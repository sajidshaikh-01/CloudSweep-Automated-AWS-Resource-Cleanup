terraform {
  required_version = ">= 1.0"

  backend "s3" {
    bucket         = "cronda-tf-state-sajid"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "cronda-tf-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}
