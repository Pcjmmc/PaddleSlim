docker run -d --name=paddletest_nginx_server  --net=host \
    -v /paddletest/app/paddletest/backend/nginx.conf:/etc/nginx/nginx.conf\
    nginx:latest\
    /bin/bash -c "
    nginx -g 'daemon off;'
    "