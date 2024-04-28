FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY data /app/data
COPY src /app/src
COPY main.py /app/main.py

CMD ["python", "main.py"]
