#!/usr/bin/env bash
# Bash script to set up web servers for the deployment of web_static

if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config_file="/etc/nginx/sites-available/default"
sudo sed -i '/^\tlocation \/hbnb_static {/a\\t\talias /data/web_static/current/;' "$config_file"
sudo sed -i '/^\tlocation \/hbnb_static {/a\\t\tindex index.html index.htm;' "$config_file"

sudo service nginx restart
