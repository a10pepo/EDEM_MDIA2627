FROM python:3.12-slim

WORKDIR /app

COPY . . 
RUN pip install requests psycopg2-binary

CMD ["python", "renfe_collector.py"]