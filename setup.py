# coding=utf-8
import os
import codecs
from setuptools import setup, find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-base-libs',
    version='1.0',
    description='Library of helpers for Django projects',
    long_description = read('README.md'),
    author='Aidas Bendoraitis',
    author_email='aidasbend@yahoo.com',
    url = 'https://github.com/archatas/django-base-libs',
    download_url='',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe = False,
    install_requires = [
    ],
)