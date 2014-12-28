# Snakebite  
[![Build Status](https://travis-ci.org/wheresmybento/snakebite.svg?branch=master)](https://travis-ci.org/wheresmybento/snakebite)
[![Coverage Status](https://img.shields.io/coveralls/wheresmybento/snakebite.svg)](https://coveralls.io/r/wheresmybento/snakebite)

Snakebite is built with Python, and more specifically with Falcon framework and MongoEngine (python client for MongoDB).

To get started, please follow instructions below on how to setup your environment to run Snakebite

## Instructions

First, clone this repository onto your local machine

```
$ git clone https://github.com/wheresmybento/snakebite.git
$ cd snakebite
```

We first need to install all the dependencies or packages needed (a virtualenv is recommended).

```
$ python setup.py develop
```

## Up and Running
 Assuming you are already in the project directory, simply run the following command:

```
$ gunicorn manage:snakebite.app
```

Point your browser to localhost:8000/restaurants (thereby making a GET request).
Try adding params in your URL, for instance, http://localhost:8000/restaurants?location=Roppongi&tags=casual

To try a POST request, you can do the following via the Terminal:

```
$ curl -X  POST -H "Content-Type:application/json" -d '{"name": "yoshinoya", "location": "tsukiji"}' http://localhost:8000/restaurants
```

Of course, you may prefer to use POSTMAN.io (easy GUI) to make these POST request. That is fine too.
Do note that Snakebite only accepts json [content-type](http://en.wikipedia.org/wiki/Internet_media_type) for POST requests.

## Testing & Contributing

Before pushing codes, please ensure that the code is checked against flake8 firstly

```
$ python setup.py flake8
```

Next, to check tests and coverage reports, do the following:

```
$ coverage run setup.py nosetests
```

Let's try to keep the code clean with Flake8, and less bug-free with testing!
Target coverage: 80%

## DEPLOYING

When deploying to environments other than your local environment ('dev'), please ensure that you set the 'BENRI_ENV' environment variable in the OS before running the server.
This is so that the right config file can be loaded for initializing the application.


## TODO

1. Setup MongoDB and models
