#!/bin/bash
sudo -s source .venv/bin/activate;
python manage.py makemigrations;
python manage.py migrate;
yes yes | python manage.py collectstatic;
sudo chmod 777 ./db.sqlite3
sudo chmod 777 ./
sudo chown :www-data ./db.sqlite3
sudo chown :www-data ./
sudo service apache2 restart
echo "Done";
