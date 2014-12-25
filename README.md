# Snakebite  [![Build Status](https://travis-ci.org/wheresmybento/snakebite.svg?branch=master)](https://travis-ci.org/wheresmybento/snakebite)

Snakebite is built with Python, and more specifically with Falcon framework and MongoEngine (python client for MongoDB).

To get started, please follow instructions below on how to setup your environment to run Snakebite

## Instructions

First, clone this repository onto your local machine

```
$ git clone https://github.com/wheresmybento/snakebite.git
$ cd snakebite
```

We first need to install all the dependencies or packages needed.
You may prefer to setup a virtual env first for better package management.

```
$ python setup.py develop
```

## Example app

Once dependencies are installed, we just need to run the server!

```
$ cd snakebite
$ gunicorn example:api
```

Point your browser to `http://localhost:8000/restaurants``` to see the example json response from our code!

> Note that this is just an example app to show you the rough idea of buliding with Falcon.

To run the actual application, do the following commands:

```
/* if you are not in the uppermost 'snakebite' directory */
$ cd ..
$ gunicorn runserver:app
```

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
2. tests
3. use colander for management of requests
4. controllers to be used instead of a one-python-file app.
