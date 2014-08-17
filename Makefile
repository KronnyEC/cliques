all: clean test www app

prod: clean test www_prod app_prod link_libs

build_frontend_prod:
	grunt --gruntfile frontend/Gruntfile.js prod

build_frontend:
	grunt --gruntfile frontend/Gruntfile.js

www_prod: build_frontend_prod
	grunt --gruntfile frontend/Gruntfile.js www

www: build_frontend
	grunt --gruntfile frontend/Gruntfile.js www

app_prod: build_frontend_prod
	grunt --gruntfile frontend/Gruntfile.js app

app: build_frontend
	grunt --gruntfile frontend/Gruntfile.js app

link_libs:
	mkdir -p libs
	bash install_libs.sh

test:
	grunt --gruntfile frontend/Gruntfile.js csslint
	tox -epep8
	#tox -edjango

clean_www:
	rm -rf www/*

clean_app:
	rm -rf cordova/www/*

clean_build:
	rm -rf frontend/build/*

clean: clean_www clean_app clean_build

install_ubuntu:
	sudo apt-get install python-dev git python-pip mysql-server mysql  libmysqlclient-dev mysql-python

install_osx:
	brew install git pip mysql
	mysql.server start

install:
	npm install -g grunt grunt-cli bower
	cd frontend/ && npm install
	cd frontend/ && bower install
	pip install tox
	tox -e dev
#	msyql -u$MYSQL_USER -p$MYSQL_PASSWORD -e 'create database IF NOT EXISTS cliques'
        DJANGO_SETTINGS_MODULE="cliques.settings" python manage.py help
	DJANGO_SETTINGS_MODULE="cliques.settings" dev/bin/python manage.py syncdb --noinput
	DJANGO_SETTINGS_MODULE="cliques.settings" dev/bin/python manage.py migrate --noinput

sync_appengine:
#	source prod_exports
	bin/python manage.py syncdb
	bin/python manage.py migrate

deploy: sync_appengine
	appcfg.py update .

rollback:
	appcfg.py rollback .

serve:
	dev_appserver.py dev.yaml

staging:
	dev_appserver.py staging.yaml

whoopee:
	echo "Sorry, I'm not in the mood"

