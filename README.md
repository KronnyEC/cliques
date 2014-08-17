cliques
=======

A private social network focused on small (under 25 people) groups.

1. Install the necessary system packages: `make install`. You can run `make install_ubuntu` or `make install_osx` to install system packages first.

1. Create a 'cliques' database in your database with: `mysql -uroot -p` then `create database cliques`. Note:
we're running cliques database as root. Don't do this in production.

1. Activate the python virtual environment: `source dev/bin/activate`

1. Install the database tables: `python manage.py syncdb`

1. Finally, run the database schema migrations: `python manage.py migrate`.

To run the App Engine dev server, run `dev_appserver.py app.yaml` in the root directory of this project.

Running `make test` will run the entire test suite, both the Django backend and the frontend. Travis will run these tests on commit as well.

[![Build Status](https://travis-ci.org/pcsforeducation/cliques.svg?branch=master)](https://travis-ci.org/pcsforeducation/cliques)

[ ![Codeship Status for pcsforeducation/cliques](https://codeship.io/projects/0fb2e970-0825-0132-8774-7a8fe1d63f6e/status)](https://codeship.io/projects/31328)

