FROM python:3-alpine
WORKDIR /app
RUN pip install boto3
COPY cloudwatch-query-exec-logs.py .

CMD ["python", "cloudwatch-query-exec-logs.py"]
