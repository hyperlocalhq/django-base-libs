from __future__ import absolute_import

from datetime import datetime

from huey.contrib.djhuey import db_task, task, periodic_task

'''
start the huey consumer with this command:
$ ./manage.py run_huey

queue a task with the following commands:
>>> from ccb.apps.async_test.tasks import *
>>> result = add(2, 2)

if you want to wait synchronously for the result, use the blocking .get method:
>>> result.get()  # (time passes...)
4
'''

@task()
def hello_world():
    s = ('Hello World')
    print('{} - {}'.format(
        datetime.now(),
        s,
    ))
    return s


@task()
def add(x, y):
    s = x + y
    print('{} - {}'.format(
        datetime.now(),
        s,
    ))
    return s


@task()
def mul(x, y):
    s = x * y
    print('{} - {}'.format(
        datetime.now(),
        s,
    ))
    return s


@task()
def xsum(numbers):
    s = sum(numbers)
    print('{} - {}'.format(
        datetime.now(),
        s,
    ))
    return s
