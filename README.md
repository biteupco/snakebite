# Snakebite  
[![Build Status](https://travis-ci.org/gobbl/snakebite.svg?branch=master)](https://travis-ci.org/gobbl/snakebite)

Snakebite is built with Python, and more specifically with Falcon framework and MongoEngine (python client for MongoDB).

To get started, please follow instructions below on how to setup your environment to run Snakebite

## Prerequisite

###Linux (apt-get)

python [setuptools](https://pypi.python.org/pypi/setuptools)
```
$ sudo apt-get install python-setuptools
```

python-dev 
```
$ sudo apt-get install python-dev
```
mongo-db [Ubuntu](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/) / [Debian](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-debian/)

Import the public key used by the package management system.
```
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
```
Create a list file for MongoDB.
```
$ echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
```
Reload local package database.
```
$ sudo apt-get update
```
Install the MongoDB packages.
```
$ sudo apt-get install -y mongodb-org
```

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

Before running the application, we need to have our database up. Do `$sudo mongod`.
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

Next, to check tests and coverage reports:

1. Ensure MongoDB is running on your local machine. To start MongoDB: `$ sudo mongod`

2. Run the tests by doing: `$ coverage run setup.py nosetests`

Let's try to keep the code clean with Flake8, and less bug-free with testing!
Target coverage: 80% (current: 100%)

## DEPLOYING

When deploying to environments other than your local environment ('dev'), please ensure that you set the 'BENRI_ENV' environment variable in the OS before running the server.
This is so that the right config file can be loaded for initializing the application.
