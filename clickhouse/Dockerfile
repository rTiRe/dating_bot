FROM python:3.12-slim

WORKDIR /clickhouse

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# вариант 1: shell-форма
# CMD sleep 10 && python main.py

# вариант 2: exec-форма с вызовом shell
# CMD ["sh", "-c", "sleep 10 && python main.py"]
CMD ["python", "main.py"]
