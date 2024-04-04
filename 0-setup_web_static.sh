#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static.

# Install Nginx if it not already installed
if ! [ -x "$(command -v nginx)" ]; then
	sudo apt update
	sudo apt install -y nginx

fi

# Creating the directories if they don't exist
sudo mkdir -p /data/web_static/shared/
echo "/data/web_static/shared/ dir created"
sudo mkdir -p /data/web_static/releases/test/
echo "/data/web_static/releases/test/"

# Creating an html file
echo "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

echo "HTML file created"

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership recursively to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo bash -c 'cat <<EOF > /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF'

# Restart Nginx
sudo service nginx restart
