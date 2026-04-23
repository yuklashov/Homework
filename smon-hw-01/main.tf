data "yandex_compute_image" "debian_latest" {
  family = "debian-11"
}

resource "yandex_compute_instance" "vm-1" {
  name                      = "smon-hw-01-vm"
  platform_id               = "standard-v3" # Intel Ice Lake
  zone                      = var.yc_zone
  allow_stopping_for_update = true

  resources {
    cores         = 2
    memory        = 1
    core_fraction = 20
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.debian_latest.id
      size     = 3
    }
  }

  scheduling_policy {
    preemptible = true
  }

  network_interface {
    subnet_id = "e9b458hv8thgf4tn8skc"
    nat       = true
  }

  metadata = {
    user-data = "#cloud-config\nusers:\n  - name: ${var.vm_user}\n    groups: sudo\n    shell: /bin/bash\n    sudo: ['ALL=(ALL) NOPASSWD:ALL']\n    ssh-authorized-keys:\n      - ${var.ssh_key_public}\n"
  }
}

variable "vm_user" {
  description = "VM user name"
  type        = string
  default     = "admin"
}

variable "ssh_key_public" {
  description = "Public SSH key for the VM"
  type        = string
  sensitive = true
}
