flask-boilerplate
=================

Boilerplate to speedup flask development with best practices.


Project Status
--------------

- **develop** branch:

Heroku deployment: https://flbp.herokuapp.com/

[![Build Status](https://travis-ci.org/teracyhq/flask-boilerplate.svg?branch=develop)](https://travis-ci.org/teracyhq/flask-boilerplate)
[![Coverage Status](https://coveralls.io/repos/teracyhq/flask-boilerplate/badge.png?branch=develop)](https://coveralls.io/r/teracyhq/flask-boilerplate?branch=develop)

- **master** branch:

[![Build Status](https://travis-ci.org/teracyhq/flask-boilerplate.svg?branch=master)](https://travis-ci.org/teracyhq/flask-boilerplate)
[![Coverage Status](https://coveralls.io/repos/teracyhq/flask-boilerplate/badge.png?branch=master)](https://coveralls.io/r/teracyhq/flask-boilerplate?branch=master)


Installation
------------

Use `teracy-dev`: http://dev.teracy.org/docs/getting_started.html

Then:

```
$ ws
$ cd personal
$ git clone git@github.com:teracyhq/flask-boilerplate.git
$ cd flask-boilerplate
$ mkvirtualenv flask-boilerplate
$ make resolve
```


Configuration
-------------

See `flask-boilerplate/app/config.py`


Usage
-----

**Run**

```
$ python manage.py db setup
$ python manage.py runserver -h 0.0.0.0
```

Then open: http://localhost:5000/ to see how the app works.

**Test**


```
$ make test-unit
```

to run unit tests

or:

```
$ make test-intg
```

to run integration tests
 
or:

```
$ make test
```

to run both unit and integration tests


after that, `$ make report-coverage` to see coverage report.


**Style**

```
$ make check-style
```

to check pep8, pylint styles.


Contributing
------------

- File issues at https://issues.teracy.org/browse/<project_key>

- Follow Teracy's workflow at http://dev.teracy.org/docs/workflow.html

Discussions
-----------

Join us:

- https://groups.google.com/forum/#!forum/teracy

- https://www.facebook.com/groups/teracy

Get our news:

- https://www.facebook.com/teracyhq

- https://twitter.com/teracyhq


Author and contributors
-----------------------

See more details at `AUTHORS.md` and `CONTRIBUTORS.md` files.


License
-------

BSD License

```
Copyright (c) Teracy, Inc. and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Teracy, Inc. nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

```
