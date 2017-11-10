import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='pyramid_default_cors',
    version='0.2',
    description='Default wiring for CORS XHR',
    long_description=README,
    author='Mark Floyd',
    author_email='mark@goodrx.com',
    url='https://github.com/emfloyd2/pyramid_default_cors',
    keywords='config web wsgi pyramid',
    packages=find_packages(),
    zip_safe=False,
)
