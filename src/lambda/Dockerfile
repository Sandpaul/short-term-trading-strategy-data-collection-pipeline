# lambda Dockerfile

# Dockerfile

FROM public.ecr.aws/lambda/python:3.11

# Copy the function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Command can be overwritten by providing a different command in the template.yaml
CMD ["lambda_function.lambda_handler"]
