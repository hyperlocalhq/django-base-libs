# -*- coding: UTF-8 -*-
from fabric.api import env, run, prompt, local, get, sudo, settings
from fabric.colors import red, green
from fabric.state import output

env.environment = ""
env.full = False

output['running'] = False

PRODUCTION_HOST = "museumsportal-berlin.de"
PRODUCTION_USER = "museumsportal"


def dev():
    """ chooses development environment """
    env.environment = "dev"
    env.hosts = [PRODUCTION_HOST]
    env.user = PRODUCTION_USER
    print("LOCAL DEVELOPMENT ENVIRONMENT\n")


def staging():
    """ chooses testing environment """
    env.environment = "staging"
    env.hosts = ["museumsportal.jetsonproject.org"]
    env.user = "museumsportal"
    print("STAGING WEBSITE\n")


def production():
    """ chooses production environment """
    env.environment = "production"
    env.hosts = [PRODUCTION_HOST]
    env.user = PRODUCTION_USER
    print("PRODUCTION WEBSITE\n")


def full():
    """ all commands should be executed without questioning """
    env.full = True


def _update_dev():
    """ updates development environment """
    run("")  # password request
    print

    if env.full or "y" == prompt(red('Get latest production database (y/n)?'), default="y"):
        print(green(" * creating production-database dump..."))
        run('cd ~/db_backups/ && ./backupdb.bsh --latest')
        print(green(" * downloading dump..."))
        get("~/db_backups/db_latest.sql", "tmp/db_latest.sql")
        print(green(" * importing the dump locally..."))
        local('python manage.py dbshell < tmp/db_latest.sql && rm tmp/db_latest.sql')
        print
        if env.full or "y" == prompt('Call prepare_dev command (y/n)?', default="y"):
            print(green(" * preparing data for development..."))
            local('python manage.py prepare_dev')
    print

    if env.full or "y" == prompt(red('Download media uploads (y/n)?'), default="y"):
        print(green(" * creating an archive of media uploads..."))
        run('cd ~/project/museumsportal/media/ '
            '&& tar -cz -f ~/project/museumsportal/tmp/media.tar.gz *')
        print(green(" * downloading archive..."))
        get("~/project/museumsportal/tmp/media.tar.gz",
            "tmp/media.tar.gz")
        print(green(" * extracting and removing archive locally..."))
        for host in env.hosts:
            local('cd media/ '
                '&& tar -xzf ../tmp/media.tar.gz '
                '&& rm tmp/media.tar.gz')
        print(green(" * removing archive from the server..."))
        run("rm ~/project/museumsportal/tmp/media.tar.gz")
    print

    if env.full or "y" == prompt(red('Update code (y/n)?'), default="y"):
        print(green(" * updating code..."))
        local('git pull')
    print

    if env.full or "y" == prompt(red('Migrate database schema (y/n)?'), default="y"):
        print(green(" * migrating database schema..."))
        local("python manage.py migrate --no-initial-data")
        local("python manage.py syncdb")
    print


def _update_staging():
    """ updates testing environment """
    run("")  # password request
    print

    if env.full or "y" == prompt(red('Set under-construction screen (y/n)?'), default="y"):
        print(green(" * Setting maintenance screen"))
        run('cd ~/public_html/ '
            '&& cp .htaccess_under_construction .htaccess')
    print

    if env.full or "y" == prompt(red('Stop cron jobs (y/n)?'), default="y"):
        print(green(" * Stopping cron jobs"))
        with settings(user="root"):
            run('/etc/init.d/cron stop')
    print

    if env.full or "y" == prompt(red('Get latest production database (y/n)?'), default="y"):
        print(green(" * creating production-database dump..."))
        run('cd ~/db_backups/ && ./backupdb.bsh --latest')
        print(green(" * downloading dump..."))
        run("scp %(user)s@%(host)s:~/db_backups/db_latest.sql ~/db_backups/db_latest.sql" % {
            'user': PRODUCTION_USER,
            'host': PRODUCTION_HOST,
        })
        print(green(" * importing the dump locally..."))
        run('cd ~/project/museumsportal/ && python manage.py dbshell < ~/db_backups/db_latest.sql')
        print
        if env.full or "y" == prompt(red('Call prepare_staging command (y/n)?'), default="y"):
            print(green(" * preparing data for testing..."))
            run('cd ~/project/museumsportal/ '
                '&& python manage.py prepare_staging')
    print

    if env.full or "y" == prompt(red('Get latest media uploads (y/n)?'), default="y"):
        print(green(" * updating media uploads..."))
        run("scp -r %(user)s@%(host)s:~/project/museumsportal/media/* ~/project/museumsportal/media/" % {
            'user': PRODUCTION_USER,
            'host': PRODUCTION_HOST,
        })
    print

    if env.full or "y" == prompt(red('Update code (y/n)?'), default="y"):
        print(green(" * updating code..."))
        run('cd ~/project/museumsportal '
            '&& git pull')
    print

    if env.full or "y" == prompt(red('Collect static files (y/n)?'), default="y"):
        print(green(" * collecting static files..."))
        run('cd ~/project/museumsportal '
            '&& python manage.py collectstatic --noinput')
    print

    if env.full or "y" == prompt(red('Migrate database schema (y/n)?'), default="y"):
        print(green(" * migrating database schema..."))
        run('cd ~/project/museumsportal '
            '&& python manage.py migrate --no-initial-data')
        run('cd ~/project/museumsportal '
            '&& python manage.py syncdb')
    print

    if env.full or "y" == prompt(red('Restart webserver (y/n)?'), default="y"):
        print(green(" * Restarting Apache"))
        with settings(user="root"):
            run('/etc/init.d/apache2 graceful')
    print

    if env.full or "y" == prompt(red('Start cron jobs (y/n)?'), default="y"):
        print(green(" * Starting cron jobs"))
        with settings(user="root"):
            run('/etc/init.d/cron start')
    print

    if env.full or "y" == prompt(red('Unset under-construction screen (y/n)?'), default="y"):
        print(green(" * Unsetting maintenance screen"))
        run('cd ~/public_html/ '
            '&& cp .htaccess_live .htaccess')
    print


def _update_production():
    """ updates production environment """
    if "y" != prompt(red('Are you sure you want to update ' + red('production', bold=True) + ' website (y/n)?'), default="n"):
        return

    run("")  # password request
    print

    if env.full or "y" == prompt(red('Set under-construction screen (y/n)?'), default="y"):
        print(green(" * Setting maintenance screen"))
        run('cd ~/public_html/ '
            '&& cp .htaccess_under_construction .htaccess')
    print

    if env.full or "y" == prompt(red('Stop cron jobs (y/n)?'), default="y"):
        print(green(" * Stopping cron jobs"))
        with settings(user="root"):
            run('/etc/init.d/cron stop')
    print

    if env.full or "y" == prompt(red('Backup database (y/n)?'), default="y"):
        print(green(" * creating a database dump..."))
        run('cd ~/db_backups/ '
            '&& ./backupdb.bsh')
    print

    if env.full or "y" == prompt(red('Update code (y/n)?'), default="y"):
        print(green(" * updating code..."))
        run('cd ~/project/museumsportal/ '
            '&& git pull')
    print

    if env.full or "y" == prompt(red('Collect static files (y/n)?'), default="y"):
        print(green(" * collecting static files..."))
        run('cd ~/project/museumsportal '
            '&& python manage.py collectstatic --noinput')
    print

    if env.full or "y" == prompt(red('Migrate database schema (y/n)?'), default="y"):
        print(green(" * migrating database schema..."))
        run('cd ~/project/museumsportal '
            '&& python manage.py migrate --no-initial-data')
        run('cd ~/project/museumsportal '
            '&& python manage.py syncdb')
    print

    if env.full or "y" == prompt(red('Restart webserver (y/n)?'), default="y"):
        print(green(" * Restarting Apache"))
        with settings(user="root"):
            run('/etc/init.d/apache2 graceful')
    print

    if env.full or "y" == prompt(red('Start cron jobs (y/n)?'), default="y"):
        print(green(" * Starting cron jobs"))
        with settings(user="root"):
            run('/etc/init.d/cron start')
    print

    if env.full or "y" == prompt(red('Unset under-construction screen (y/n)?'), default="y"):
        print(green(" * Unsetting maintenance screen"))
        run('cd ~/public_html/ '
            '&& cp .htaccess_live .htaccess')
    print


def deploy():
    """ updates the chosen environment """
    if not env.environment:
        while env.environment not in ("dev", "staging", "production"):
            env.environment = prompt(red('Please specify target environment ("dev", "staging", or "production"): '))
            print

    globals()["_update_%s" % env.environment]()