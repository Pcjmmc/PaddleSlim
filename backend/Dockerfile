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
COPY ./conf/nginx.conf /etc/nginx/nginx.conf

COPY requirements.txt /app/

RUN pip install --proxy http://172.19.57.45:3128 -r /app/requirements.txt

# WORKDIR /home/app/backend/
# RUN pip install -r requirements.txt

# EXPOSE 8999

# CMD ["/usr/local/bin/supervisord", "-n", "-c", "/home/app/backend/supervisor/supervisord.conf"]

