# transform/Dockerfile

FROM python:3.12.5-slim

WORKDIR /app

COPY src/transform/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/transform/ /app/src/transform/
COPY src/utils/ /app/src/utils/

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "transform.transform_and_save_data"]