# Trabajo de Diploma para Esteban Acevedo Santana como Ingeniero en Automática

> ## Objetivo
>  Desarrollar un sistema de medición de bajo costo con un sensor espectroscópico basado en Raspberry Pi y ESP32
>  Desplegar en la Raspberry Pi un servidor en Python para crear una red neuronal capaz de detectar cambios en los sistemas, utilizando Django como framework y TensorFlow como librería de aprendizaje automático
>  Utilizar esta red neuronal en dispositivos de bajo costo, específicamente en un ESP32

> [Docuemtno de Tesis](https://drive.google.com/drive/folders/1xj-vwUddcT_fEKV6P6z_GX1HAFPx-lOL?usp=sharing) 

# ![imagen](https://github.com/user-attachments/assets/4993c8ee-dfe1-4580-b3fd-26097c63f596)
# ![imagen](https://github.com/user-attachments/assets/800d3536-b1eb-4344-ae1d-cc91dd664812)
# 

# ![imagen](https://github.com/user-attachments/assets/7223c793-f344-458f-aea8-e69f456a3451)





# Configuraciones para los sistemas enbebidos 

## Configuraciones de raspberry para desplegar django-adaminlte-3 en apache2
* `sudo apt-get update`
* `sudo apt-get install apache2`
* `sudo apt-get install libapache2-mod-wsgi-py3`

## Venv
* `sudo apt-get install python3-pip`
* `sudo pip install virtualenv`
* `pip install virutalenv`
* `virtualenv .venv`
* `source .venv/bin/activate`
* `pip install -r requirements.txt`

## Django
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py collectstatic`



## Apache2

### WSGIDaemonProcess en nuevo puerto

### Deshabilitar sitio(en caso de querer usar puertos ya creados)
* `sudo a2dissite file.conf`
### Cambiar Puerto en 'ports.conf'
* `Listen ##`
### Crear fichero 'file.conf' en 'sities-available'
``` 
<VirtualHost *:##>
	Alias /static/ /path/static/
	<Directory /path/static>
		Require all granted
	</Directory>

	WSGIScriptAlias / /path/config/wsgi.py
	WSGIDaemonProcess django python-path=/path python-home=/path/.venv
	WSGIProcessGroup django
	WSGIScriptAlias / /path/config/wsgi.py

	<Directory /path/config>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>
</VirtualHost>
```
* `sudo a2ensite file.conf`
* `sudo systemctl reload apache2`

## WSGIPythonHome en puerto default apache
* `sudo nano /etc/apache2/sites-available/000-default.conf`
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
* `sudo service apache2 restart`

### I2c permisos
* `sudo usermod -aG i2c www-data`
* `sudo systemctl restart apache2`
#### Agregar o descomentar en '/boot/config.txt'
* `dtparam=i2c_arm=on`

### Pip Adicionales
* `pip install flatbuffers==23.5.26`


### OS Pprmisos
* `sudo chmod 664 ./db.sqlite3`
* `sudo chmod 777 ./`
* `sudo chmod 777 /home/<user>` 
* `sudo chmod 777 ./media` 
* `sudo chown :www-data ./db.sqlite3`
* `sudo chown :www-data ./`
* `sudo service apache2 restart`

