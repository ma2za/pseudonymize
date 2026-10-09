FROM python:3.12-slim
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /var/task
COPY requirements.txt ./requirements.txt
COPY wheels/ ./wheels/
RUN pip install --no-cache-dir --no-index --find-links=./wheels --require-hashes -r requirements.txt && rm -rf wheels
COPY src/ ./src/
COPY server.py ./server.py
COPY model/ ./model/
ARG ENGINE_COMMIT=unknown
ENV ENGINE_COMMIT=${ENGINE_COMMIT} PYTHONPATH=/var/task:/var/task/src MODEL_DIR=/var/task/model PORT=8080
EXPOSE 8080
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
