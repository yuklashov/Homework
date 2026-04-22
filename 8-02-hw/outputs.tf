output "jenkins_ip" {
  description = "Public IP address of Jenkins VM"
  value       = yandex_compute_instance.jenkins.network_interface.0.nat_ip_address
}

output "nexus_ip" {
  description = "Public IP address of Nexus VM"
  value       = yandex_compute_instance.nexus.network_interface.0.nat_ip_address
}
