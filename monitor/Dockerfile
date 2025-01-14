FROM python:3.9-slim
WORKDIR /app
COPY monitor.py .
RUN apt-get update -y && apt-get install -y iputils-ping
RUN pip install pymysql psutil flask
EXPOSE 5000
CMD ["python", "monitor.py"]
