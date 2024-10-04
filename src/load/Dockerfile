# load/Dockerfile

FROM python:3.12.5-slim

WORKDIR /app

COPY src/load/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/load/ /app/src/load/
COPY src/utils/read_parquet_from_s3.py /app/src/utils/

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "load.load"]