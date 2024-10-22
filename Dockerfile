# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .