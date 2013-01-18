Getting started
===============

#. Run following to have your local settings::

    cp local_settings.py.def local_settings.py


#. Have your database configuration set up in ``local_settings.py``


#. Create a database in your mysql server with following SQL::

    CREATE DATABASE hexic CHARACTER SET utf8;


#. Run following to create tables in your database. Make sure you **don't** create
   admin user::

    python manage.py syncdb

   It will create inital data in ``initial_data.json``


#. Run the server with::

    python manage.py runserver


#. You can now access ``http://localhost:8000``


#. Also you can access admin page ``http://localhost:8000/admin``


Extra commands
===============
- To remove all .pyc files run::

    find . -name "*.pyc" -exec rm {} \;

- To run tests::

    python manage.py test -v 2 api game public security admin

  ``-v 2`` is the verbosity level. Allowed values are 0=minimal output, 1=normal output, 2=all output

- To run specific tests::

    python manage.py test api.APITest.test_new_msj

- To create new account by SMS::
    wget -O - 'http://localhost:8000/api/?phone=%2B976596&msg=(Tand%2099437911%20dugaaraas%20100%20negj%20ilgeelee)'


South commands
===============
- For first migration::
    
    ./manage.py schemamigration app_name --initial

- Other time::
    
    ./manage.py schemamigration app_name --auto

- To apply this migration::

   ./manage.py migrate app_name
