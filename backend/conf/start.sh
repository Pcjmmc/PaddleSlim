docker run -d --name=paddletest_nginx_server_test  --net=host \
    -v /paddletest/app/conf:/home/app/backend\
    -w /home/app/backend \
    ce_web_backend:backend_v1\
    /bin/bash -c "
    cp /home/app/backend/nginx.conf  /etc/nginx/nginx.conf
    export http_proxy=http://172.19.57.45:3128
    export https_proxy=http://172.19.57.45:3128
    pip install -r requirements.txt
    unset https_proxy
    unset http_proxy
    /usr/local/bin/supervisord -n -c /home/app/backend/supervisor/nginx/supervisord.conf
    "