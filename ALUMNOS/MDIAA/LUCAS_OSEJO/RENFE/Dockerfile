
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV ALERT_DISTANCE_METERS=1000
ENV POLL_SECONDS=15

CMD ["python", "renfe_collector.py"]