# Stage 1: Сборка React-приложения
FROM node:18 AS builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Python-контейнер с FastAPI
FROM python:3.10-slim
WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код FastAPI (main.py и пр.) в контейнер
COPY . .

# Копируем собранные статические файлы React в папку проекта
COPY --from=builder /app/frontend/build /app/frontend/build

# Открываем порт и запускаем Uvicorn
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
