#!/bin/bash

# Проверка на привилегии root
if [ "$(id -u)" -ne 0 ]; then
  echo "Этот скрипт должен быть запущен от имени root."
  exit 1
fi

# Команда, которая будет выполняться на хосте
COMMAND="$@"

# Запуск команды на хосте через Docker
docker run --rm -v /:/mnt alpine sh -c "chroot /mnt sh -c \"$COMMAND\""
