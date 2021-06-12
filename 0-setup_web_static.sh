#!/usr/bin/env bash
#  deploy static

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
sudo service nginx start

sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

sudo echo "TURTLES" | sudo tee /data/web_static/releases/test/index.html

sudo ln -fs /data/web_static/releases/test/ /data/web_static/current

sudo chown -hR ubuntu:ubuntu /data/

# edit nginex config file
target="^\tlocation / {"
sendit="\tlocation /hbnb_static/ {\n\
\t\talias /data/web_static/current/;\n\t}\n\n\tlocation / {"
sudo sed -i "s@${target}@${sendit}@" /etc/nginx/sites-available/default

sudo service nginx restart

exit 0
