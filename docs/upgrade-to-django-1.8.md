# Upgrade to Django 1.8 and Django CMS 3.4

## 1. Set under construction screen

    $ cd ~/public_html
    $ cp .htaccess_under_construction .htaccess

## 2. Disable cron jobs

    $ cd ~
    $ crontab empty_crontab

## 3. Backup database

    $ cd ~/commands
    $ ./backup_db_now.sh

## 4. Update git

    $ cd ~
    $ . bin/activate
    $ cd project/ccb
    $ git pull

## 5. Upgrade pip and install requirements

    $ pip install --upgrade pip
    $ pip install --upgrade setuptools
    $ pip install -r requirements.txt

## 6. Set up secrets.json

    $ nano ~/project/ccb/settings/secrets.json

Copy and paste the settings there from local file

## 7. Delete *.PYC files

    $ cd ~
    $ find . -name "*.pyc" -exec rm -f {} \;

## 8. Run migrations and fix cms tree

    $ cd ~/project/ccb/
    $ echo "UPDATE django_migrations SET app='social_django' WHERE app='default';" | python manage.py dbshell --settings=settings.production
    $ python manage.py migrate contenttypes --settings=settings.production
    $ python manage.py migrate social_django 0003_alter_email_max_length --fake --settings=settings.production
    $ python manage.py migrate --settings=settings.production
    $ python manage.py cms fix-tree --settings=settings.production

## 9. Collect static files

    $ cd ~/project/ccb/
    $ python manage.py collectstatic --settings=settings.production

## 10. Change my.wsgi

    $ nano ~/public_html/my.wsgi

Change "settings" to "settings.production"

## 11. Check the website under allowed IP

See if the IP in .htaccess matches yours.

    $ sudo restart_apache

Browse through the website to see if media files are loading and there are not other obvious errors.

## 12. Unset under construction screen

    $ cd ~/public_html
    $ cp .htaccess_live .htaccess

## 13. Enable cron jobs

    $ cd ~
    $ crontab crontab

## 14. Enjoy

Play your favourite song and have fun!