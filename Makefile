all: clean test www app

build_frontend:
	grunt --gruntfile frontend/Gruntfile.js

www: build_frontend
	grunt --gruntfile frontend/Gruntfile.js www

app: build_frontend
	grunt --gruntfile frontend/Gruntfile.js
	grunt --gruntfile frontend/Gruntfile.js app

test:
	grunt --gruntfile frontend/Gruntfile.js csslint
	tox -epep8
	#tox -edjango

clean:
	grunt --gruntfile frontend/Gruntfile.js clean

install_ubuntu:
	sudo apt-get install python-dev git python-pip mysql-server mysql  libmysqlclient-dev mysql-python

install_osx:
	brew install git pip mysql
	mysql.server start

install:
	sudo pip install tox
	tox -e dev
	msyql -uroot -p -e 'create database cliques'
	dev/bin/python manage.py syncdb
	dev/bin/python manage.py migrate

whoopee:
	echo "Sorry, I'm not in the mood"
