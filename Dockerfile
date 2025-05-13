# Dockerfile

FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем список зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём папку для диалогов
RUN mkdir -p dialogues

# Открываем порт и запускаем Uvicorn
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
