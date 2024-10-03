# transform/Dockerfile

FROM public.ecr.aws/lambda/python:3.11

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/local/bin/aws-lambda-rie
RUN chmod +x /usr/local/bin/aws-lambda-rie

WORKDIR /app

COPY src/transform/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/transform/ /app/src/transform/
COPY src/utils/ /app/src/utils/

ENV PYTHONPATH=/app/src

ENTRYPOINT ["/usr/local/bin/aws-lambda-rie", "python3", "-m", "awslambdaric"]

CMD ["transform.transform_and_save_data.transform_and_save_data"]
