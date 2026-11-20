FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY renfe_collector.py schema.sql sample_flotaLD.json ./

# Usuario sin privilegios
RUN useradd --create-home appuser
USER appuser

# Valores por defecto; se sobrescriben con `docker run -e ...`
ENV ALERT_DISTANCE_METERS=5000 \
    POLL_INTERVAL_SECONDS=30 \
    MAX_POSITION_AGE_SECONDS=300 \
    LOG_LEVEL=INFO

CMD ["python", "renfe_collector.py"]
