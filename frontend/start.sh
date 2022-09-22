docker run -d --name=paddle_quality_web_frontend  --net=host \
         -v /home/disk1/app/paddletest/frontend:/home/app/frontend\
         -w /home/app/frontend \
        ce_web_frontend:frontend_v1\
        /bin/bash -c "
        cp /home/app/frontend/nginx.conf /etc/nginx/nginx.conf
        nginx -g 'daemon off;'
        "