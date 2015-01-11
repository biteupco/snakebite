# Snakebite UI Client

## Introduction

This Node JS client is meant to provide a simple web UI (re: HTML) to interact with the Snakebite server. 

Snakebite is meant to be a html-less, simple RESTful json-loving' API server that can talk to many various client. It was never meant to talk HTML.


Instead of the terminal (via `curl`) or the wonderful [Postman.io](http://www.getpostman.com), we now get to look at and interact with nice HTML from the Snakebite UI client then.


## Basic Setup

1. Ensure that you have Snakebite API Server and MongoDB running first.
2. Install [Node](http://nodejs.org/download/) on your machine, if you have not already done so.
3. Assuming you are in the main project directory, `cd` into this UI directory by doing ```$ cd ui```
4. Install all node dependancies by issuing the command `$ sudo npm install`. Sudo is needed for installing [Express JS]()
5. run the Snakebite UI client via ```$ node ./bin/www```
6. If you point your brower to http://localhost:3000, you should see a similar page as this:

![main page screenshot](main_page_screenshot.png)
