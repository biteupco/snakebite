#!/bin/bash

if [ "$SNAKEBITE" == "CMS" ]; then
  node ui/bin/www
else
  gunicorn manage:snakebite.app
fi