This is an open-source tool for creating a database of sources. 

(hat tip to [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04))

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

	CREATE USER sourcelistuser WITH PASSWORD 'password-here'

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








