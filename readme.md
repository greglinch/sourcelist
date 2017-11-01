This is an open-source tool for creating a database of sources. 

(hat tip to Digital Ocean [Django](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04) and [Postgres](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04))

The following instructions are intended for Ubuntu 16.

# Prep the system

	sudo apt-get update
	sudo apt-get install python3-pip
	sudo apt-get install git
	sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

# Install virtualenvwrapper

Install packages 

	sudo -H pip3 install --upgrade pip
	sudo -H pip3 install virtualenv virtualenvwrapper

For Python3 and pip3

	echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc

Finalize the process

	echo "export WORKON_HOME=~/Env" >> ~/.bashrc
	echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

Execute the bash script

	source ~/.bashrc

# Set up the database

Enter the database shell 

	sudo -u postgres psql

Create the database

	CREATE DATABASE sourcelist;

Create the user

	CREATE USER sourcelistuser WITH PASSWORD 'password-here';

Grant permissions

	GRANT ALL PRIVILEGES ON DATABASE sourcelist TO sourcelistuser;

Close the shell

	\q

# Set up GitHub

Generate ssh key 

	ssh-keygen -t rsa -b 4096 -C "youremail"

# Set up the project

Make the virtual environment

	mkvirtualenv sourcelist

Clone the repo (or your fork)

	git clone git@github.com:greglinch/sourcelist.git

Change into the directory

	cd sourcelist

Install the requirements

	pip3 install -r requirements.txt

Add the private settings file

	vim sourcelist/settings_private.py

Paste the following (and fill all the `UPDATE` vars)

	## private settings

	SECRET_KEY = '' # UPDATE

	ALLOWED_HOSTS = [
	    # local
	    '127.0.0.1',
	    # prod
	    '', # UPDATE
	    # test
	    '', # UPDATE
	]
	INTERNAL_IPS = ['127.0.0.1']

	## for local and test servers
	TEST_ENV = True
	## for prod server
	# TEST_ENV = False

	## project info

	PROJECT_NAME = '' # UPDATE
	EMAIL_SENDER = '' # UPDATE
	SITE_URL = '' # UPDATE

	## database
	db_engine = ''  # UPDATE
	db_name = '' # UPDATE
	db_user = '' # UPDATE
	db_password = '' # UPDATE
	db_host = '' # UPDATE
	db_port = '' # UPDATE

	## email
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_HOST = # UPDATE
	EMAIL_PORT = # UPDATE
	EMAIL_HOST_USER = '' # UPDATE
	EMAIL_HOST_PASSWORD = '' # UPDATE
	EMAIL_USE_TLS = True
	DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

	## social auth
	SOCIAL_AUTH_PASSWORDLESS = True
	SOCIAL_AUTH_ALWAYS_ASSOCIATE = True

	SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '' # UPDATE
	SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '' # UPDATE

	SOCIAL_AUTH_TWITTER_KEY = '' # UPDATE 
	SOCIAL_AUTH_TWITTER_SECRET = '' # UPDATE

	# SOCIAL_AUTH_FACEBOOK_KEY = '' # UPDATE
	# SOCIAL_AUTH_FACEBOOK_SECRET = '' # UPDATE
	# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

Initial migration for admin tables

    python3 manage.py migrate

Initial migration for the app

    python3 manage.py makemigrations sources
    python3 manage.py migrate

Create a super user

    python3 manage.py createsuperuser

Collect static assets

    python3 manage.py collectstatic

Update the firewall permissions

    sudo ufw allow 8080

Test the local server

    python3 manage.py runserver 0.0.0.0:8080

Then navigate to the live site

	domain.com:8080

Stop the local server

    Ctrl + C

## Set up uWSGI application server

Exit your virtualenv

    deactivate

Install key pieces 

    sudo -H pip3 install uwsgi

Make directory for sites

    sudo mkdir -p /etc/uwsgi/sites

Make the ini file

    sudo vim /etc/uwsgi/sites/sourcelist.ini

Paste in these settings

    [uwsgi]

    logto = /var/log/uwsgi/error.log

    project = sourcelist
    uid = ubuntu
    base = /home/%(uid)

    chdir = %(base)/%(project)
    home = %(base)/Env/%(project)
    module = %(project).wsgi:application

    master = true
    processes = 5

    socket = /run/uwsgi/%(project).sock
    chown-socket = %(uid):www-data
    chmod-socket = 660
    vacuum = true

Create a systemd unit file 

    sudo vim /etc/systemd/system/uwsgi.service

Paste this 

    [Unit]
    Description=uWSGI Emperor service

    [Service]
    ExecStartPre=/bin/bash -c 'mkdir -p /run/uwsgi; chown ubuntu:www-data /run/uwsgi'
    ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    NotifyAccess=all

    [Install]
    WantedBy=multi-user.target

## Set up nginx reverse proxy cache

Install nginx 

    sudo apt-get install nginx

Create a config file

    sudo vim /etc/nginx/sites-available/sourcelist

Add this

    server {
        listen 80;
        server_name YOUR-DOMAIN.COM;
        access_log /var/log/nginx/sourcelist_access.log;
        error_log /var/log/nginx/sourcelist_error.log;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static/ {
            root /home/ubuntu/sourcelist/;
        }

        location / {
            include         uwsgi_params;
            uwsgi_pass      unix:/run/uwsgi/sourcelist.sock;
        }
    }

Remove the symlink for the default site

    sudo rm /etc/nginx/sites-enabled/default

Symlink the available site to an enable site

    sudo ln -s /etc/nginx/sites-available/sourcelist /etc/nginx/sites-enabled

Check the configuration

    sudo nginx -t

## Server final prep

Restart nginx

    sudo systemctl restart nginx

Start uwsgi
    
    sudo systemctl start uwsgi

Update the firewall rules

    sudo ufw delete allow 8080
    sudo ufw allow 'Nginx Full'

Enable uwsgi and nginx to run on startup

    sudo systemctl enable nginx
    sudo systemctl enable uwsgi

## Let's Encrypt CertBot

For example:

	https://certbot.eff.org/#ubuntuxenial-nginx
