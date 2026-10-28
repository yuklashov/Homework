# apache_role

Роль восстановлена из старого apache_role.tar.gz и уточнена по условию SYS-62. Целевые ОС — Debian/Ubuntu с systemd; контроллер может быть Mac. Требуется community.general для необязательного правила UFW.

Параметры: apache_manage_ufw=false, apache_disk_name="", apache_document_root=/var/www/html. Веб-страница содержит CPU, RAM, первый диск, IP и hostname из ansible_facts. Для конкретного диска задайте apache_disk_name.

Handler перезапуска вызывается только изменением 000-default.conf; изменение index.html не перезапускает сервер. После flush_handlers модуль uri проверяет HTTP 200. UFW меняется только при apache_manage_ufw=true; ошибки не скрываются. Межсетевые экраны облака роль не меняет.

В октябре 2026 выполнялись только syntax-check и локальный рендер шаблона; это не подтверждение развёртывания роли на Linux.
