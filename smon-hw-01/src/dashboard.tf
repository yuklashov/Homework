terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "= 0.201.0"
    }
  }
}
provider "yandex" {
  folder_id = var.folder_id
}
variable "folder_id" {
  type = string
}
variable "vm_id" {
  type = string
}
resource "yandex_monitoring_dashboard" "cpu" {
  name  = "smon-cpu-example"
  title = "CPU utilization"
  widgets {
    position {
      x = 0
      y = 0
      w = 12
      h = 6
    }
    chart {
      title    = "CPU utilization, %"
      chart_id = "cpu"
      queries {
        target {
          query     = "{service=\"compute\", name=\"cpu_utilization\", resource_id=\"${var.vm_id}\"}"
          text_mode = true
        }
      }
    }
  }
}
