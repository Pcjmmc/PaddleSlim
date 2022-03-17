docker run -d --name=paddle_quality_web_frontend  --net=host \
         -v /ssd1/app/paddletest/frontend:/home/app/frontend\
         -e "http_proxy=http://172.19.56.199:3128" \
         -e "https_proxy=http://172.19.56.199:3128" \
         -w /home/app/frontend \
        ce_web_frontend:frontend_v1\
        /bin/bash -c "
        cp /home/app/frontend/nginx.conf /etc/nginx/nginx.conf
        nginx -g 'daemon off;'
        "