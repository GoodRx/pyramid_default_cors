from setuptools import find_packages
from setuptools import setup

setup(
    name='pyramid_default_cors',
    version='0.2.1',
    description='Default wiring for CORS XHR',
    long_description_markdown_filename='README.md',
    author='Mark Floyd',
    author_email='mark@goodrx.com',
    url='https://github.com/GoodRx/pyramid_default_cors',
    keywords='config web wsgi pyramid',
    packages=find_packages(),
    zip_safe=False,
    setup_requires=[
        'setuptools-markdown >= 0.2, < 1.0',
    ],
)
