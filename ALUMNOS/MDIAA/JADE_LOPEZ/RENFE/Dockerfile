FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY renfe_collector.py api.py .
CMD ["python", "-u", "renfe_collector.py"]