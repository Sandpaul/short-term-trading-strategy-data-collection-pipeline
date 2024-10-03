# lambda/Dockerfile

FROM python:3.12.5-slim

WORKDIR /app

# Copy and install requirements
COPY src/lambda/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the function code
COPY src/lambda/ /app/src/lambda/

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Set the CMD to invoke the correct Lambda handler
CMD ["python", "-m", "lambda.lambda_function"]
