FROM   nginx
LABEL Description="Built For Ce web Frontend " Maintainer="paddle-dev@baidu.com"
# Install Dependence
RUN apt-get update && apt-get -y install procps && apt-get -y install vim \
    \
# Create Journal Directory
    && mkdir -p /home/app/logs/nginx && mkdir -p /home/app/frontend
# Copy Service Profile
COPY nginx.conf /etc/nginx/nginx.conf
# # Copy Dist
# COPY dist /home/app/frontend/dist
# # Start container
# EXPOSE 8081
# CMD ["nginx", "-g", "daemon off;"]