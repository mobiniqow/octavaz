#!/bin/bash
# make directory 
sudo mkdir -p "/var/html/www/octavaz/static/" 
sudo chmod -R 777 "/var/html/www/octavaz/static/"
sudo mkdir -p "/var/log/octavaz" 
sudo touch  "/var/log/octavaz/access.log"  
echo "static directory created"

sudo mkdir -p "/var/html/www/octavaz/media/"
sudo chmod -R 777 "/var/html/www/octavaz/media/"
echo "media directory created"

sudo mkdir -p "/var/html/www/octavaz/template/"
sudo chmod -R 777 "/var/html/www/octavaz/template/"

echo "template directory created"

# create database
sudo chmod +X create_db.sh
sh ./create_db.sh
cd /home/ubuntu/octavaz

# deploy database
sudo  cp ./octavaz.config  /etc/nginx/sites-available/octavaz
sudo ln -sf /etc/nginx/sites-available/octavaz  /etc/nginx/sites-enabled/octavaz
sudo  cp ./octavaz.service  /etc/systemd/system/octavaz.service
echo "template directory created"
sudo  cp ./octavaz.socket  /etc/systemd/system/octavaz.socket
echo "template directory created"
sudo systemctl daemon-reload

python -m pip install pip

pip install -q -r req.txt

sudo nginx -t

sudo systemctl restart nginx

echo "sudo systemctl restart"
sudo systemctl restart octavaz.socket
sudo systemctl restart octavaz.service

sudo systemctl enable  octavaz.socket
sudo systemctl restart octavaz.service

black .

python manage.py makemigrations --settings core.settings.prod
python manage.py migrate --settings core.settings.prod
python manage.py collectstatic --no-input --settings core.settings.prod

sudo certbot --nginx -d octavaz.ir -d www.octavaz.ir
sudo systemctl restart nginx
echo "done"
