# transform/Dockerfile

FROM public.ecr.aws/lambda/python:3.11

# Add AWS Lambda Runtime Interface Emulator for local testing
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/local/bin/aws-lambda-rie
RUN chmod +x /usr/local/bin/aws-lambda-rie

WORKDIR /app

# Install requirements
COPY src/transform/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/transform/ /app/src/transform/
COPY src/utils/ /app/src/utils/

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Use RIE when running locally
ENTRYPOINT ["/usr/local/bin/aws-lambda-rie", "python3", "-m", "awslambdaric"]

# Set the CMD to invoke the correct Lambda handler
CMD ["transform.transform_and_save_data.transform_and_save_data"]
