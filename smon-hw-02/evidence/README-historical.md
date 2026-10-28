# Домашнее задание к занятию «Система мониторинга Zabbix» - Юклашов

## Задание 1. Установка Zabbix Server

### Текст использованных команд:
```bash
wget https://repo.zabbix.com/zabbix/6.0/debian/pool/main/z/zabbix-release/zabbix-release_6.0-4+debian11_all.deb
sudo dpkg -i zabbix-release_6.0-4+debian11_all.deb
sudo apt update

sudo apt install -y zabbix-server-pgsql zabbix-frontend-php php7.4-pgsql zabbix-apache-conf zabbix-sql-scripts zabbix-agent postgresql

sudo -u postgres psql -c "CREATE USER zabbix WITH PASSWORD 'zabbix';"
sudo -u postgres createdb -O zabbix zabbix

zcat /usr/share/zabbix-sql-scripts/postgresql/server.sql.gz | sudo -u zabbix psql zabbix

sudo sed -i 's/# DBPassword=/DBPassword=zabbix/' /etc/zabbix/zabbix_server.conf

sudo systemctl restart zabbix-server zabbix-agent apache2
sudo systemctl enable zabbix-server zabbix-agent apache2
```

### Скриншот авторизации в админке:
> [!NOTE]
> *(Здесь нужно вставить скриншот входа в веб-интерфейс Zabbix)*
> `![Вход в Zabbix](link-to-screenshot)`

---

## Задание 2. Установка Zabbix Agent

### Текст использованных команд для второго хоста:
```bash
wget https://repo.zabbix.com/zabbix/6.0/debian/pool/main/z/zabbix-release/zabbix-release_6.0-4+debian11_all.deb
sudo dpkg -i zabbix-release_6.0-4+debian11_all.deb
sudo apt update
sudo apt install -y zabbix-agent

# Вместо 192.168.1.100 подставляется IP сервера Zabbix
sudo sed -i 's/Server=127.0.0.1/Server=192.168.1.100/' /etc/zabbix/zabbix_agentd.conf
sudo sed -i 's/ServerActive=127.0.0.1/ServerActive=192.168.1.100/' /etc/zabbix/zabbix_agentd.conf
sudo sed -i 's/Hostname=Zabbix server/Hostname=ZabbixAgent-Host2/' /etc/zabbix/zabbix_agentd.conf

sudo systemctl restart zabbix-agent
sudo systemctl enable zabbix-agent
```

### Скриншот раздела Configuration > Hosts:
> [!NOTE]
> *(Здесь нужно вставить скриншот со списком хостов, где статус Zabbix агента зелёный)*
> `![Хосты](link-to-screenshot)`

### Скриншот лога zabbix agent:
> [!NOTE]
> *(Здесь нужно вставить скриншот или вывод `cat /var/log/zabbix/zabbix_agentd.log`)*
> `![Логи агента](link-to-screenshot)`

### Скриншот раздела Monitoring > Latest data:
> [!NOTE]
> *(Здесь нужно вставить скриншот метрик обоих серверов)*
> `![Latest Data](link-to-screenshot)`
