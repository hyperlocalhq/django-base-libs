# -*- coding: UTF-8 -*-
'''
This script helps automate the creation of random instances of the models that should generate email notifications.

In order to use it, please keep in mind the following requirements:
- AutoFixture should be installed:
    $ pip install django-autofixture
- AutoFixture should be enabled:
    INSTALLED_APPS should include 'autofixture'
- Redis should be running:
    $ redis-server
- MailHog should be running:
    $ MailHog
- Celery should be running:
    $ ./manage.py celeryd --beat --loglevel=INFO
- Optionally, if you want to monitor pending tasks, run the Celery Camera:
    $ ./manage.py celery events --camera=djcelery.snapshot.Camera

On FreeBSD, both Celery processes are managed by supervisorctl. Here are some example commands (must be root):
    # supervisorctl status
    celery_beat                      STOPPED    Apr 14 04:58 PM
    celery_camera                    STOPPED    Apr 14 04:58 PM

    # supervisorctl start all
    celery_camera: started
    celery_beat: started

    # supervisorctl status
    celery_beat                      RUNNING    pid 39455, uptime 0:00:33
    celery_camera                    RUNNING    pid 39456, uptime 0:00:33

    # supervisorctl restart all
    celery_camera: stopped
    celery_beat: stopped
    celery_beat: started
    celery_camera: started

    # supervisorctl tail celery_beat
    ...

    # supervisorctl tail celery_beat stderr
    ...

Remember that for MailHog intercept sent emails, you need to configure Django for it. Add the following to your local_settings.py:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

If go and MailHog are not installed, first install go. On FreeBSD, it's simply:
    $ pkg install go
and on Mac it's
    $ brew install go
Once go is installed, install MailHog:
    $ go get github.com/mailhog/MailHog
Remember to set $GOPATH, and to add $GOPATH/bin to your PATH.

To check whether object creation results in sending emails, open the MailHog web console, available by default at http://localhost:8025.
'''

from autofixture import AutoFixture

from actstream.actions import follow

from ccb.apps.people.models import Person
from ccb.apps.events.models import Event
from ccb.apps.marketplace.models import JobOffer
from ccb.apps.bulletin_board.models import Bulletin
from ccb.apps.institutions.models import Institution
from jetson.apps.comments.models import Comment
from jetson.apps.individual_relations.models import IndividualRelation
from jetson.apps.messaging.models import InternalMessage
from ccb.apps.tracker.models import Ticket

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from jetson.apps.notification.models import NoticeType
from jetson.apps.notification.tasks import get_notification_setting

from base_libs.middleware.threadlocals import set_current_user

reinhard_user = User.objects.get(username='reinhard_knobelspies')
aidas_user = User.objects.get(username='aidas')
reinhard = Person.objects.get(user__username='reinhard_knobelspies')
aidas = Person.objects.get(user__username='aidas')

set_current_user(aidas_user)

studio38 = Institution.objects.get(title='studio 38')
studio38_content_type = ContentType.objects.get_for_model(studio38)

uf = AutoFixture(User)
ef = AutoFixture(Event, field_values={
    'organizing_institution': studio38,
    'venue': studio38,
    'organizing_person': aidas,
})
jf = AutoFixture(JobOffer, field_values={
    'offering_institution': studio38,
    'contact_person': aidas,
})
bf = AutoFixture(Bulletin, field_values={
    'institution': studio38,
    # 'contact_person': aidas,
})
iif = AutoFixture(Institution, field_values={

})
cf = AutoFixture(Comment, field_values={
    'user': aidas.user,
    'content_type': studio38_content_type,
    'object_id': studio38.pk,
})
irf = AutoFixture(IndividualRelation, field_values={
    'user': aidas.user,
})
mf = AutoFixture(InternalMessage, field_values={
    'creator': aidas.user,
    'sender': aidas.user,
    # 'submitter_name': aidas.user.get_full_name(),
    # 'submitter_email': aidas.user.email,
    # 'modifier': aidas.user,
})
tf = AutoFixture(Ticket, field_values={
    'submitter': aidas.user,
    'submitter_name': aidas.user.get_full_name(),
    'submitter_email': aidas.user.email,
    # 'modifier': aidas.user,
    'content_type': studio38_content_type,
    'object_id': studio38.pk,
})

notice_types = list(NoticeType.objects.all())
settings = []
us = uf.create(4)
frequencies = '''never immediately daily weekly'''.split()
user_frequencies = zip(us, frequencies)
for user, frequency in user_frequencies:
    user.username = 'notify_{}'.format(frequency)
    user.save()
    follow(user, studio38)
    follow(user, aidas)
    person = Person.objects.get(user=user)
    person.person_repr = user.username
    person.status = 'published'
    person.save()
    for notice_type in notice_types:
        setting = get_notification_setting(user, notice_type, "1")
        setting.frequency = frequency
        setting.save()
        settings += [(
            setting.frequency,
            setting.user,
            setting.notice_type,
            setting.medium,
        )]

e = ef.create(1)[0]
j = jf.create(1)[0]
b = bf.create(1)[0]
#ii = iif.create(1)[0]
c = cf.create(1)[0]
#ir = irf.create(1)[0]
m = mf.create(1)[0]
t = tf.create(1)[0]

