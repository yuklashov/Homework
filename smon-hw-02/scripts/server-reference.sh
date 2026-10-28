#!/usr/bin/env bash
# Справочная последовательность для чистой Debian 12; здесь не выполнялась.
set -euo pipefail
wget 'https://repo.zabbix.com/zabbix/7.4/release/debian/pool/main/z/zabbix-release/zabbix-release_7.4-4+debian12_all.deb' -O /tmp/zabbix-release.deb
sudo dpkg -i /tmp/zabbix-release.deb
sudo apt update
sudo apt install -y postgresql zabbix-server-pgsql zabbix-frontend-php php-pgsql zabbix-apache-conf zabbix-sql-scripts zabbix-agent zabbix-get
sudo systemctl enable --now postgresql
sudo -u postgres createuser --pwprompt zabbix
sudo -u postgres createdb -O zabbix zabbix
schema_file=$(dpkg -L zabbix-sql-scripts | sed -n '\|/postgresql/server.sql.gz$|p')
test -n "$schema_file" && test -f "$schema_file"
zcat "$schema_file" | sudo -u zabbix psql -v ON_ERROR_STOP=1 zabbix
# Задать DBHost/DBName/DBUser/DBPassword приватно, не помещать пароль в shell history.
sudoedit /etc/zabbix/zabbix_server.conf
# Установить и проверить конфиги агентов из src под реальные адреса.
sudo systemctl enable --now zabbix-server zabbix-agent apache2
sudo systemctl restart zabbix-server zabbix-agent apache2
