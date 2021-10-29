# Dockerfile
FROM python:3.8
WORKDIR /backend
COPY . /backend
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
