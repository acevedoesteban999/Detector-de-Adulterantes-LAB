# Djagno-Adminlte Raspberry


## Configuracion de repsberry para desplegar django-adaminlte3 en apache2

`sudo apt-get update`
`sudo apt-get install apache2`
`sudo apt-get install libapache2-mod-wsgi-py3`

### venv
`sudo apt-get install python3-pip`
`sudo pip install virtualenv`
`pip install virutalenv`
`virtualenv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`


### apache2
`sudo nano /etc/apache2/sites-available/000-default.conf`

```
<VirtualHost *:80>
    #...
</VirtualHost>
#STATIC
Alias /static/ /project/static/
<Directory /project/static>
    Require all granted
</Directory>

#MEDIA
Alias /media/ /project/media/
<Directory /project/media>
    AllowOverride None
    Require all granted
</Directory>

#WSGI
WSGIScriptAlias / /project/app/wsgi.py
WSGIPythonHome /project/.venv
WSGIPythonPath /project
<Directory /project/app>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>
```

`chmod 664 ~/project/db.sqlite3`
`sudo chown :www-data ~/project/db.sqlite3`
`sudo chown :www-data ~/project`
`sudo service apache2 restart`