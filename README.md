cliques
=======

A private social network focused on small (under 25 people) groups.

To run tests, install tox `sudo pip install tox` then run `tox -e dev` to create your dev environment. Then run `bash install_libs.sh` to symlink your installed libraries
to a place that App Engine can access them. 

To run the App Engine dev server, run `dev_appserver.py app.yaml` in the root directory of this project.

Running `tox` will run the entire test suite. Travis will run these tests on commit as well.

[![Build Status](https://travis-ci.org/pcsforeducation/cliques.svg?branch=master)](https://travis-ci.org/pcsforeducation/cliques)
