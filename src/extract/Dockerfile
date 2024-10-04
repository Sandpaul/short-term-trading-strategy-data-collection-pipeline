# extract/Dockerfile

FROM python:3.12.5-slim

WORKDIR /app

COPY src/extract/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/extract/ /app/src/extract/
COPY src/utils/save_to_s3_as_parquet.py /app/src/utils/

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "extract.extract_and_save_data"]