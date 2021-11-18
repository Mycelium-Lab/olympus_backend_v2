# Dockerfile
FROM python:3.8
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
WORKDIR /backend
COPY . /backend
COPY ./notifications /notifications
CMD ["/usr/bin/supervisord"]
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]