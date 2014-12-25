# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from Cython.Build import cythonize
from distutils.extension import Extension


def read_file(filename):
    with open(filename, 'r') as infile:
        return infile.read()

requires = [
    "falcon==0.2.0b1",
    "Cython==0.21.1",
    "colander==1.0",
    "mongoengine==0.8.7",
    "gunicorn==18.0"
]

extras_require = {
    "test": [
        "nose",
        "coverage",
        "flake8",
        "mock"
    ]
}

setup(name='snakebite',
    version='0.1.0',
    ext_modules=cythonize([
        Extension(
            'bin.papi.papi',
            sources=['bin/papi/papi.py'],
            extra_compile_args=["-O3", "-Wall", "-Wno-strict-prototypes"]
        ),
    ]),
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
    extras_require=extras_require,
)
