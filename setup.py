import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="django_postgres_vault",
    version="0.1.2",
    url="https://github.com/jciskey/django_postgres_vault",
    license='MIT',

    author="Joe Ciskey",
    author_email="jciskey@inceptivecss.com",

    description="A simple Django database backend that allows rotating access credentials via HashiCorp Vault",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',

    packages=find_packages(exclude=('tests',)),

    install_requires=[
        'Django>=3.0',
        'hvac',
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
    ],
)
