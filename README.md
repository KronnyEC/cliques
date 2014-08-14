cliques
=======

A private social network focused on small (under 25 people) groups.

1. Install the necessary system packages: `sudo apt-get install python-dev git`

1. First, install tox `sudo pip install tox`

1. Then run `tox -e dev` to create your dev environment.

1. Run `bash install_libs.sh` to symlink your installed Python libraries to a place that App Engine can access them. 

1. Create a 'cliques' database in your database with: `mysql -uroot -p` then `create database cliques`. Note:
we're running cliques database as root. Don't do this in production.

1. Activate the python virtual environment: `source dev/bin/activate`

1. Install the database tables: `python manage.py syncdb`

1. Finally, run the database schema migrations: `python manage.py migrate`.

To run the App Engine dev server, run `dev_appserver.py app.yaml` in the root directory of this project.

Running `make test` will run the entire test suite, both the Django backend and the frontend. Travis will run these tests on commit as well.

[![Build Status](https://travis-ci.org/pcsforeducation/cliques.svg?branch=master)](https://travis-ci.org/pcsforeducation/cliques)
