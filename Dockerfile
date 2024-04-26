FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY data /app/data
COPY src /app/src
COPY main.py /app/main.py

CMD ["python", "main.py"]