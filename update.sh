#!/bin/bash
sudo -s source .venv/bin/activate;
python manage.py makemigrations;
python manage.py migrate;
yes no | python manage.py collectstatic;
#chmod 777 update.sh
sudo chmod 777 ./db.sqlite3
sudo chmod 777 ./
sudo chown :www-data ./db.sqlite3
sudo chown :www-data ./
sudo service apache2 restart
echo "Done";
