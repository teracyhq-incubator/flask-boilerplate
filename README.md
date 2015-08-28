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


REST APIs
---------

Flask-Boilerplate focuses on REST APIs driven development. There are built-in endpoints of `users`
and `roles`.

We use [HTTPie](https://github.com/jkbrzt/httpie) and
[httpie-jwt-auth](https://github.com/teracyhq/httpie-jwt-auth) plugin for testing.

To install `HTTPie` and `httpie-jwt-auth`, please follow:

```
$ pip install --upgrade httpie
$ pip install --upgrade httpie-jwt-auth
```

Note: should use `sudo` to install for system wide usage.

after that: `$ http --version` should print out: `0.9.2` or something similar on the screen.

**/api/versions**

```
$ http :5000/api/versions -v
GET /api/versions HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.2



HTTP/1.0 200 OK
Content-Length: 302
Content-Type: application/json; charset=utf-8
Date: Tue, 25 Aug 2015 18:02:02 GMT
Server: Werkzeug/0.10.4 Python/2.7.6
Set-Cookie: session=eyJfaWQiOnsiIGIiOiJOakZoTXpKaU5tTXpZelpqWlRReFpEWmtPRFUxTlRrM1pqazFPRFU0TWpFPSJ9fQ.CL4_Gg.EHh4Ipnc24t_maZ29rkNPxFEYhU; HttpOnly; Path=/

{
    "latest": {
        "info": "developing version, APIs are expected to change and break things", 
        "status": "@", 
        "version": "v1.0"
    }, 
    "supported": [
        {
            "info": "developing version, APIs are expected to change and break things", 
            "status": "@", 
            "version": "v1.0"
        }
    ]
}

```

**/api/v1.0/users**

- To create a new user:

```
$ http POST :5000/api/v1.0/users email=admin@teracy.com password=123456 -v
POST /api/v1.0/users HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 51
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.2

{
    "email": "admin@teracy.com", 
    "password": "123456"
}

HTTP/1.0 201 CREATED
Content-Length: 422
Content-Type: application/json; charset=utf-8
Date: Wed, 26 Aug 2015 03:40:50 GMT
Location: http://localhost:5000/api/v1.0/users/1
Server: Werkzeug/0.10.4 Python/2.7.6
Set-Cookie: session=eyJfaWQiOnsiIGIiOiJOakZoTXpKaU5tTXpZelpqWlRReFpEWmtPRFUxTlRrM1pqazFPRFU0TWpFPSJ9fQ.CL7Gwg.aIDJrepymtCif8S9ktd3MLHhOfs; HttpOnly; Path=/

{
    "data": {
        "active": true, 
        "confirmed_at": "2015-08-26T03:40:50+00:00", 
        "created_at": "2015-08-26T03:40:50+00:00", 
        "email": "admin@teracy.com", 
        "id": 1, 
        "roles": [
            {
                "description": "user role", 
                "id": 1, 
                "name": "user"
            }
        ], 
        "updated_at": "2015-08-26T03:40:50+00:00"
    }
}

```

**/api/v1.0/token**

- to retrieve the jwt token:

```
$ http POST :5000/api/v1.0/token email=admin@teracy.com password=123456 -v
POST /api/v1.0/token HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 51
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.2

{
    "email": "admin@teracy.com", 
    "password": "123456"
}

HTTP/1.0 200 OK
Content-Length: 238
Content-Type: application/json; charset=utf-8
Date: Wed, 26 Aug 2015 03:45:54 GMT
Server: Werkzeug/0.10.4 Python/2.7.6
Set-Cookie: session=eyJfaWQiOnsiIGIiOiJOakZoTXpKaU5tTXpZelpqWlRReFpEWmtPRFUxTlRrM1pqazFPRFU0TWpFPSJ9fQ.CL7H8g.O2eBChbsZEacjpfEfBtpOu-lyzE; HttpOnly; Path=/

{
    "expires_in": 7200, 
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0NDA1NjA3NTQsInB3ZCI6ImMwYjQ0MTEwZjEwOWYwZGRmZDQ2NDNlM2M4NDRiNzIwIiwic3ViIjoxLCJleHAiOjE0NDA1Njc5NTR9.5nLH7uOBxjISIgTRlqXEJmJxA_A9171ip9KM3uS2kKo"
}
```

After that, the token should be use to access token required resources.

For example:

```
$ http --auth-type=jwt --auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0NDA1NjA3NTQsInB3ZCI6ImMwYjQ0MTEwZjEwOWYwZGRmZDQ2NDNlM2M4NDRiNzIwIiwic3ViIjoxLCJleHAiOjE0NDA1Njc5NTR9.5nLH7uOBxjISIgTRlqXEJmJxA_A9171ip9KM3uS2kKo: :5000/api/v1.0/users/me -v
GET /api/v1.0/users/me HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0NDA1NjA3NTQsInB3ZCI6ImMwYjQ0MTEwZjEwOWYwZGRmZDQ2NDNlM2M4NDRiNzIwIiwic3ViIjoxLCJleHAiOjE0NDA1Njc5NTR9.5nLH7uOBxjISIgTRlqXEJmJxA_A9171ip9KM3uS2kKo
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.2



HTTP/1.0 200 OK
Content-Length: 422
Content-Type: application/json; charset=utf-8
Date: Wed, 26 Aug 2015 03:48:06 GMT
Server: Werkzeug/0.10.4 Python/2.7.6
Set-Cookie: session=eyJfaWQiOnsiIGIiOiJOakZoTXpKaU5tTXpZelpqWlRReFpEWmtPRFUxTlRrM1pqazFPRFU0TWpFPSJ9fQ.CL7Idg.oDFRMTszTfmSxl1hvNLVaIxUwg0; HttpOnly; Path=/

{
    "data": {
        "active": true, 
        "confirmed_at": "2015-08-26T03:40:50+00:00", 
        "created_at": "2015-08-26T03:40:50+00:00", 
        "email": "admin@teracy.com", 
        "id": 1, 
        "roles": [
            {
                "description": "user role", 
                "id": 1, 
                "name": "user"
            }
        ], 
        "updated_at": "2015-08-26T03:40:50+00:00"
    }
}

```


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
