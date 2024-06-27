# Используем базовый образ Python
FROM python:3.12.3

# Установка зависимостей системы
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        python3-dev \
        musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка переменной среды для Python
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /code

# Копирование зависимостей проекта и установка их
COPY requirements.txt /code/

RUN pip install -r requirements.txt

# Копирование всего остального кода проекта
COPY . /code/

# Определение команды для запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
