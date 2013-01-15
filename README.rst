Getting started
===============

#. Run following to have your local settings::

    cp local_settings.py.def local_settings.py


#. Have your database configuration set up in ``local_settings.py``


#. Create a database in your mysql server with following SQL::

    CREATE DATABASE hexic CHARACTER SET utf8;


#. Run following to create tables in your database::

    python manage.py syncdb


Extra commands
===============
- To remove all .pyc files run::

    find . -name "*.pyc" -exec rm {} \;

- To run tests::

    python manage.py test -v 2 api game public security

  ``-v 2`` is the verbosity level. Allowed values are 0=minimal output, 1=normal output, 2=all output

- To run specific tests::

    python manage.py test api.APITest.test_new_msj
