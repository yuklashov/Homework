terraform {
  required_version = ">= 1.4, < 2.0"
}

variable "topic" {
  type    = string
  default = "Terraform"
}

resource "terraform_data" "demo" {
  input = {
    topic = var.topic
    hosts = [for i in range(2) : format("web-%02d", i + 1)]
  }
}

output "demo" {
  value = terraform_data.demo.output
}
