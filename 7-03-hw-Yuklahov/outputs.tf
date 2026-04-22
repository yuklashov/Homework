output "bastion_vm_public_ip" {
  description = "Public IP address of the bastion VM"
  value       = yandex_compute_instance.bastion_vm.network_interface.0.nat_ip_address
}

output "web_vm_internal_ips" {
  description = "Internal IP addresses of the web VMs"
  value = {
    for vm in yandex_compute_instance.web_vm :
    vm.name => vm.network_interface.0.ip_address
  }
}
