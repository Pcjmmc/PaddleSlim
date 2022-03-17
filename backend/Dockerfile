FROM python:3.7.3
ENV DEPLOYMENT_TYPE 'PRODUCTION'

RUN apt-get -y update
RUN apt-get -y install nginx vim python-pip cron logrotate
RUN pip install --upgrade pip
RUN mkdir -p /home/app/backend \
             /home/app/logs/nginx/  \
             /home/app/logs/supervisor/   \
             /home/app/logs/tornado/   \
             /etc/supervisor.d/

# COPY . /home/app/backend/
COPY nginx.conf /etc/nginx/nginx.conf

# WORKDIR /home/app/backend/
# RUN pip install -r requirements.txt

# EXPOSE 8999

# CMD ["/usr/local/bin/supervisord", "-n", "-c", "/home/app/backend/supervisor/supervisord.conf"]

