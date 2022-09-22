docker run -d --name=paddle_quality_web_backend  --net=host \
    -v /home/disk1/app/paddletest/backend:/home/app/backend\
    -v /home/disk1/pts:/home/disk1/pts\
    -v /etc/localtime:/etc/localtime\
    -e "JAVA_HOME=/home/disk1/pts/tools/jdk1.8.0_181" \
    -w /home/app/backend \
    ce_web_backend:backend_v1\
    /bin/bash -c "
    cp /home/app/backend/nginx.conf  /etc/nginx/nginx.conf
    export http_proxy=http://172.19.57.45:3128
    export https_proxy=http://172.19.57.45:3128
    pip install -r requirements.txt
    unset https_proxy
    unset http_proxy
    python cron/task.py
    /usr/local/bin/supervisord -n -c /home/app/backend/supervisor/supervisord.conf
    "