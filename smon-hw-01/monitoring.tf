resource "yandex_monitoring_dashboard" "my_dashboard" {
  name        = "smon-hw-01-dashboard"
  description = "Dashboard for smon-hw-01"

  widgets {
    position {
      x = 0
      y = 0
      h = 6
      w = 12
    }
    title {
      text = "CPU Utilization"
    }
    chart {
      queries {
        target {
          query = "cpu_utilization{service=\"compute\", resource_id=\"${yandex_compute_instance.vm-1.id}\"}"
        }
      }
    }
  }
}
