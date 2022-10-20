docker run -d --name=paddle_quality_web_backend  --net=host \
    -v /paddletest/app/paddletest/backend:/home/app/backend\
    -v /paddletest/pts:/ssd1/pts\
    -v /etc/localtime:/etc/localtime\
    -e "JAVA_HOME=/ssd1/pts/tools/jdk1.8.0_181" \
    -w /home/app/backend \
    ce_web_backend:backend_v1\
    /bin/bash -c "
    export http_proxy=http://172.19.57.45:3128
    export https_proxy=http://172.19.57.45:3128
    pip install -r requirements.txt
    unset https_proxy
    unset http_proxy
    python cron/task.py
    /usr/local/bin/supervisord -n -c /home/app/backend/supervisor/server/supervisord.conf
    "