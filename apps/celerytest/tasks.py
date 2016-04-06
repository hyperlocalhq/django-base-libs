from __future__ import absolute_import

from celery import shared_task

'''
start the django-celery Camera with this command:
$ ./manage.py celery events --camera=djcelery.snapshot.Camera
or
$ celery -A ccb events -c djcelery.snapshot.Camera
See http://docs.celeryproject.org/en/latest/userguide/monitoring.html#monitoring-snapshots for more info.

start the celery daemon with this command:
$ ./manage.py celeryd -B -l INFO
or
$ celery -A ccb worker -l info

queue a task with the following commands:
>>> from ccb.apps.celerytest.tasks import *
>>> result = add.apply_async(countdown=10, args=[2, 2])

if you want to wait synchronously for the result, use the blocking .get method:
>>> result.get()  # (time passes...)
4
'''

@shared_task
def hello_world():
    print('Hello World')


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
