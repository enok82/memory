FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p ./frontend
RUN curl -L https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js -o ./frontend/alpine.min.js

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
