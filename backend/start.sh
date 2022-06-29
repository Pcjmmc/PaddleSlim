docker run -d --name=paddle_quality_web_backend  --net=host \
    -v /ssd1/app/paddletest/backend:/home/app/backend\
    -v /etc/localtime:/etc/localtime\
    -w /home/app/backend \
    ce_web_backend:backend_v1\
    /bin/bash -c "
    cp /home/app/backend/nginx.conf  /etc/nginx/nginx.conf
    pip install -r requirements.txt
    /usr/local/bin/supervisord -n -c /home/app/backend/supervisor/supervisord.conf
    "