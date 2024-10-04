FROM python:3.12-slim

# Install runtime interface client
RUN pip install awslambdaric

# Set the working directory
WORKDIR /app

# Copy in the application code and dependencies
COPY src/transform/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/transform/ /app/src/transform/

# Set the runtime interface client as the entrypoint
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

# Define the Lambda function handler
CMD [ "src.transform.transform_and_save_data.lambda_handler" ]
