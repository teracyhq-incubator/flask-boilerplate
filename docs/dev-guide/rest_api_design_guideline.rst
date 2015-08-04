REST API Design Guideline
=========================


Abstract
--------

We haven't got any REST APIs guidelines yet, and "consistency" is one of most important key
for Teracy development philosophy.

REST APIs are like user interface to developers. To create an open ecosystem, a friendly, robust,
easy to use is a crucial task that we MUST do it well and this documentation will help us to
design such APIs.



Introduction
------------


Resources Naming
----------------

- Nouns, not Verbs

- Compound nouns into url: `compound-nouns`

  For example: `https://api.teracy.com/finance-providers/`

Note: Avoid compound nouns, it's best to use a single word.


Media Type
----------

- By ending extension, for example: `.json`, `.xml`, etc.

- By content negotiation.

- By default, return JSON data.

If no supported media type, return 415.


Action Mapping
--------------

```
GET     - read_perm    - 200
POST    - create_perm  - 201
PUT     - update_perm  - 200
DELETE  - delete_perm  - 200
OPTIONS - help         - 200
HEAD    - read_perm without returning body content - 200
```

HTTP Codes
----------

```
200 - OK
400 - Bad Request
500 - Internal Error

201 - Created
304 - Not Modified
401 - Unauthorized
403 - Forbidden
404 - Not Found
415 - Unsupported Media Type
```

Note: consider between 403 and 404 to avoid data discovery leak.
See more: http://developer.github.com/v3/auth/#basic-authentication

CRUD
----

Successful behavior for CRUD operations:

- Create: Return 201 and `Location` header for the new created resource
- Read: Return 200 and the found resource (s)
- Update: Return 200 and the updated resource
- Delete: Return 200 and empty response

Attributes Name
---------------

Use under_score for attributes name.

- Correct     (y): `first_name`

- Incorrect   (n): `firstName` or `FirstName` or `firstname`



Error Message
-------------

HTTP error code + Error object:

```
{
  "error": {
    "code": "",
    "message": "",
    "description": "",
    "more_info": "",
    "errors": [
      {
        "code": "",
        "field": "",
        "message": ""
      }
    ]
  }
}
```

When `&suppress_response_codes=true`:

200 OK + Error object

```
{
  "error": {
    "code": "",
    "message": "",
    "description": "",
    "more_info": "",
    "errors": [],
    "status_code": {code_number}
  }
}

```

`more_info` should have a value of url for more information about the error code.

`errors` is optional and should be used to denote specific errors, helpful for validating fields
on POST or PUT.

Collections
-----------

Use `[]` for collection root.

Use `nouns` for attribute key of a collection.

Security
--------

Use `_acl` metadata for access control list.


Search
------

Global Search and scope search: `?q=`

Note: search query will be implemented with Elastic Search.


Common Reserved Query Parameters
--------------------------------

- `q`     : Search query
- `fields`: Selector specifying which fields to include in a partial response.
- `lang`: Specify language code for i18n support, default: en-us. Represents the name of a language.
          Browsers send the names of the languages they accept in the Accept-Language HTTP header
          using this format. Examples: it, de-at, es, pt-br.
- `suppress_response_codes`: true or false (1 or 0) to suspend http code, always return 200,
                             default: false (0)
- `sort`: for ordering the result set
- `until` and `since` for time-based pagination
- `before` and `after` for cursor-based pagination
- `offset` for offset-based pagination
- `limit` for pagination
- `one`: true or false (1 or 0) to expect only one result return otherwise error.
- `unique`: true or false (1 or 0) to return unique result only.
- `_method`: `put` or `delete` for POST method with a client having limited http method support
- `debug`: one of `info`, `warning`, `error` or `all`


Note: `fields` will be supported later.

Versioning
----------

Denote and define major.minor version spec only, for example: v1.0, v2.1, v3.2

Every REST endpoint must provide version resource meta data.

GET `versions`: Gets the collection of versions' meta data.

Version Entity:

- `version`: the version number

- `status`: development status, one of `@, a, b, c, f, i` that follow semantic versioning. `f` means
final and mature and `i` means inactive, deprecated.

- `info`: the additional information about the associated version

Example:

```
{
  "latest": {
    "version": "v2.0",
    "status": "f",
    "info": "latest stable version"
  },
  "supported":[
    {
      "version": "v3.0",
      "status": "@"
      "info": "developing version, APIs are expected to change and break things"
    },
    {
      "version": "v2.1",
      "status": "c2",
      "info": "release candidate 2, APIs are expected to be stable enough to use now"
    }
    {
      "version": "v1.2",
      "status": "i",
      "info": "is deprecated and will be removed by 2013-01-02, use v2.0 instead"
    }
  ]
}
```

null or empty object
--------------------

null/ None object      => `{"key": null}`

empty string           => `{"key": ""}`

empty list, collection => `{"key": []}`

empty object           => `{"key": {}}`


Date, time, timestamp
---------------------

Use ISO 8601

For example:

```
{
  "created_at": "2013-11-07T21:00:00Z"
}
```


Location
--------

Use ISO 6709

For example:

```
{
  "location": "+40.6894-074.0447"
}
```

//TODO(hoatle): consider http://geojson.org/geojson-spec.html


Batch Requests
--------------

Learn from https://developers.facebook.com/docs/reference/api/batch/


Partial Response
----------------

Follow Google's approach. For example: `?fields=title,media:group(media:thumbnail)`

https://developers.google.com/+/api/#partial-response


Pagination
----------

Follow Facebook's approach: https://developers.facebook.com/docs/graph-api/using-graph-api/v2.4#paging

Note: Offset-based Pagination is supported first, others will be supported later.

**Offset-based pagination**

Offset pagination can be used when you do not care about chronology and just want a specific number
of objects returned. This should only be used if the edge does not support cursor or time-based
pagination.

An offset-paginated edge supports the following parameters:

`offset`: This offsets the start of each page by the number specified.
`limit`:  This is the number of individual objects that are returned in each page. A limit of 0 will
          return no results. Some edges have an upper maximum on the limit value, for performance
          reasons. We will return the correct pagination links if that happens.
`next`:  The REST endpoint that will return the next page of data. If not included, this is the last
         page of data. Due to how pagination works with visibility and privacy it is possible that a
         page may be empty but contain a 'next' paging link - you should stop paging when the 'next'
         link no longer appears.
`previous`: The REST API endpoint that will return the previous page of data. If not included,
            this is the first page of data.

Note that if new objects are added to the list of items being paged, the contents of each
offset-based page will change.

Return data with:

```
{
  'data': [],
  'paging': {
    'count': X,
    'offset': X,
    'limit': X,
    'previous': 'link',
    'next': 'link',
  }
}
```

Filtering
---------

- Equal: using `field_name=value` For example: `?status=is_open&user_id=2`

- More advanced filtering, use: `field__op=value` on the query string.

  These operators should be used when appropriate:

  + eq  - equal to.                 For example: `?amount__eq=20`, the same as `?amount=20`
  + ne  - not equal to.             For example: `?amount__ne=20`
  + lt  – less than.                For example: `?amount__lt=20`
  + le  – less than or equal to.    For example: `?amount__le=20`
  + gt  – greater than.             For example: `?amount__gt=20`
  + ge  – greater than or equal to. For example: `?amount__ge=20`
  + lk  - like.                     For example: `?name__lk=%john%`
  + nl  - not like.                 For example: `?name__nl=john%`
  + in  - in.                       For example: `?name__in=john,david,joe`
  + ni  - not in.                   For example: `?name__ni=john,david,joe`
  + ct  - contains.                 For example: `?name__ct=joh`
  + mc  - match.                    For example: `?name__mc=john`


Ordering
--------

Use `sort` query param for ordering

`+` or no prefix with a field means order by field acceding.
`-` with a field means order by field descending.

for example: `?sort=id,+name,-description`


APIs Frameworks
---------------

To better design APIs, we should leverage APIs frameworks like:

- http://swagger.io/
- http://raml.org/

Those APIs frameworks have pros and cons, however, we decide to use `swagger` basing on it maturity.

And we should try others to compare with `swagger` to see when to use which frameworks.


References
----------
- http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm
- http://dev.teracy.org/docs/develop/semantic_versioning.html
- http://google-styleguide.googlecode.com/svn/trunk/jsoncstyleguide.xml
- Learn from https://apigee.com/about/api-best-practices/all/ebook
- Learn from Twitter, Facebook, Google, Foursquare, etc.
- http://devcenter.kinvey.com/rest/guides/security
- https://medium.com/@orliesaurus/a-review-of-all-most-common-api-editors-6a720dc4f4e6
- http://www.mikestowe.com/2014/07/raml-vs-swagger-vs-api-blueprint.php
- http://www.mikestowe.com/2014/12/api-spec-comparison-tool.php
- http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
- https://blog.apigee.com/detail/restful_api_design_can_your_api_give_developers_just_the_information
- http://jsonapi.org/
