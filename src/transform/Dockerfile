# transform/Dockerfile

FROM public.ecr.aws/lambda/python:3.11

WORKDIR /app

COPY src/transform/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/transform/ /app/src/transform/
COPY src/utils/ /app/src/utils/

ENV PYTHONPATH=/app/src

CMD ["transform.transform_and_save_data.transform_and_save_data"]