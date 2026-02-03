FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей (если нужно)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Переменная для пути БД
ENV DB_PATH=/app/data/app.db
ENV PYTHONPATH=/app

# Создаем папку для данных
RUN mkdir -p /app/data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]