# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


def read_file(filename):
    with open(filename, 'r') as infile:
        return infile.read()

requires = [
    "falcon==0.3.0",
    "Cython==0.22",
    "colander==1.0",
    "pymongo==2.8",
    "mongoengine==0.8.7",
    "gunicorn==18.0",
    "PyJWT==1.3.0",
]

extras_require = {
    "test": [
        "nose",
        "coverage",
        "flake8",
        "mock",
        "flake8-import-order"
    ]
}

setup(name='snakebite',
      version='0.1.0',
      description='backend server for Benri',
      long_description=read_file('README.md'),
      author='Benri',
      author_email='get.benri@gmail.com',
      keywords='web wsgi falcon restful japan',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='snakebite',
      install_requires=requires,
      extras_require=extras_require)
