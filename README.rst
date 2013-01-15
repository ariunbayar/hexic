Getting started
===============

#. Run following to have your local settings::

    cp local_settings.py.def local_settings.py

#. Have your database configuration set up in ``local_settings.py``

#. Run following to create tables in your database::

    python manage.py syncdb


Extra commands
===============
- To remove all .pyc files run::

    find . -name "*.pyc" -exec rm {} \;

