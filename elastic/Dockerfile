FROM python:3.12

WORKDIR /app

# Install system dependencies

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "elastic_service.py"]
