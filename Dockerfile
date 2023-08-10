FROM public.ecr.aws/lambda/python:3.10

COPY . ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" -U --no-cache-dir

CMD [ "app.handler" ]