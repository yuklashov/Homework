variable "yc_cloud_id" {
  description = "Yandex Cloud Cloud ID"
  type        = string
}

variable "yc_folder_id" {
  description = "Yandex Cloud Folder ID"
  type        = string
}

variable "default_zone" {
  description = "Default availability zone"
  type        = string
  default     = "ru-central1-a"
}

variable "ssh_public_key" {
  description = "SSH public key for VMs"
  type        = string
}

variable "operator_cidr" {
  description = "Адрес оператора /32, хранить в локальном tfvars"
  type        = string
  validation {
    condition     = can(cidrhost(var.operator_cidr, 0)) && endswith(var.operator_cidr, "/32")
    error_message = "Нужен IPv4 CIDR /32."
  }
}
