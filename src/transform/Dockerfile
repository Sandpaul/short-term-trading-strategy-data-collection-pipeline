# Define custom function directory
ARG FUNCTION_DIR="/function"

# Stage 1: Build the image
FROM python:3.12 as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Create the function directory
RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

# Copy the requirements file and install dependencies
COPY src/transform/requirements.txt ${FUNCTION_DIR}/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install the AWS Lambda Runtime Interface Client
RUN pip install --no-cache-dir awslambdaric

# Copy the application code
COPY src/transform/ ${FUNCTION_DIR}/src/transform/

# Stage 2: Create the final image
FROM python:3.12-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies from the previous stage
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as the default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

# Pass the name of the function handler as an argument to the runtime
CMD [ "src.transform.transform_and_save_data.transform_and_save_data" ]
