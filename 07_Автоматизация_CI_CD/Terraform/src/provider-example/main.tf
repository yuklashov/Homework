# Восстановленный минимальный пример по историческому выводу init.
# Точный исходный main.tf в архиве отсутствует. Не создаёт AWS-ресурсы.
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}
provider "aws" {
  region = "us-east-1"
}
