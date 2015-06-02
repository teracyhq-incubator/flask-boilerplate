flask-boilerplate
=================

Boilerplate to speedup flask development with best practices.


Project Status
--------------

- **develop** branch:

[![Build Status](https://travis-ci.org/teracyhq/flask-boilerplate.svg?branch=develop)](https://travis-ci.org/teracyhq/flask-boilerplate)
[![Coverage Status](https://coveralls.io/repos/teracyhq/flask-boilerplate/badge.png?branch=develop)](https://coveralls.io/r/teracyhq/flask-boilerplate?branch=develop)

- **master** branch:

[![Build Status](https://travis-ci.org/teracyhq/flask-boilerplate.svg?branch=master)](https://travis-ci.org/teracyhq/flask-boilerplate)
[![Coverage Status](https://coveralls.io/repos/teracyhq/flask-boilerplate/badge.png?branch=master)](https://coveralls.io/r/teracyhq/flask-boilerplate?branch=master)


How to develop
--------------

- Make sure `teracy-dev` is running for development environment: http://dev.teracy.org/docs/getting_started.html

- And then:

```
$ vagrant ssh
$ ws
$ cd personal
$ git clone ssh://git@code.teracy.org/clients/new-iorad.git
$ cd new-iorad
$ mkvirtualenv new-iorad
$ make resolve
```

- Create `new_iorad` database

```
$ mysql -u root -pteracy
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 468
Server version: 5.5.43-0ubuntu0.12.04.1 (Ubuntu)

Copyright (c) 2000, 2015, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> create database new_iorad;
Query OK, 1 row affected (0.01 sec)

mysql> exit

```

- export DATABASE_URL for the flask web app:

```
$ export DATABASE_URL=mysql+mysqldb://root:teracy@localhost:3306/new_iorad
```

- migrate to latest db:

```
$ python manage.py db upgrade
```

- run the app:
 
 ```
$ python manage.py runserver -h 0.0.0.0
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 ```

Then open your browser at: http://localhost:5000


Contributing
------------

- File issues at https://issues.teracy.org/browse/<project_key>

- Follow Teracy's workflow at http://dev.teracy.org/docs/workflow.html


Author and contributors
-----------------------

See more details at `AUTHORS.md` and `CONTRIBUTORS.md` files.

