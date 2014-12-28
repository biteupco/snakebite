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

Before pushing codes, please ensure the following commands below are run before pushing.

```
$ python setup.py flake8
$ python setup.py nosetest
```

Let's try to keep the code clean with Flake8, and less bug-free with testing!
Target coverage: 80%


## TODO

1. Setup MongoDB and models
