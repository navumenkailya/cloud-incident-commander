FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
# Устанавливаем FastAPI и uvicorn внутрь образа
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
# Запускаем веб-сервер uvicorn на порту 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]