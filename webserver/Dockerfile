FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask pymysql requests
CMD ["python", "app.py"]
