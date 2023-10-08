#!/usr/bin/env bash
# Sets up the server for deployment of webstatic

# Install nginx
if ! command -v nginx &> /dev/null; then
    apt-get -y update
    apt-get -y install nginx
fi

# Create required directories
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create HTML
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link
ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Nginx configuration content with proper formatting
nginx_config_content="location /hbnb_static {
    alias /data/web_static/current/;
    index index.html;
}"

# Create a temporary file with the new configuration
temp_file=$(mktemp)
awk -v content="$nginx_config_content" '!/^#/ && /server_name localhost;/ {print; print content; next} 1' /etc/nginx/sites-available/default > "$temp_file"

# Overwrite the original configuration file
mv "$temp_file" /etc/nginx/sites-available/default

# Restart nginx
service nginx restart
