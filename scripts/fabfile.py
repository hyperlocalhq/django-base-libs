from fabric.api import env, run, prompt, local, get
from fabric.state import output

PRODUCTION_CCB_DIR = "/srv/www/vhosts/creative-city-berlin.de/"
PRODUCTION_ICB_DIR = "/srv/www/vhosts/interactive-city-berlin.de/"
STAGING_CCB_DIR = "/srv/www/vhosts/test.creative-city-berlin.de/"
STAGING_ICB_DIR = "/srv/www/vhosts/test.interactive-city-berlin.de/"

env.hosts = ["creative-city-berlin.de"]
env.user = "root"
env.environment = ""
env.full = False

output['running'] = False


def dev():
    """ chooses development environment """
    env.environment = "dev"
    print("LOCAL DEVELOPMENT ENVIRONMENT\n")


def staging():
    """ chooses testing environment """
    env.environment = "staging"
    print("STAGING WEBSITE\n")


def production():
    """ chooses production environment """
    env.environment = "production"
    print("PRODUCTION WEBSITE\n")


def full():
    """ all commands should be executed without questioning """
    env.full = True


def _update_dev():
    """ updates development environment """
    run("")  # password request
    print

    if env.full or "y" == prompt('Get latest production database (y/n)?', default="y"):
        print(" * creating production-database dump...")
        run(
            'mysqldump --opt -u ccb2008 -pjkads654 ccb2008 > %sproject/jetson_project/ccb/tmp/ccb2008.sql' % PRODUCTION_CCB_DIR)
        print(" * downloading dump...")
        get("%sproject/jetson_project/ccb/tmp/ccb2008.sql"
            % PRODUCTION_CCB_DIR,
            "ccb2008.sql")
        print(" * importing the dump locally...")
        local('cd .. '
              '&& ./manage.py dbshell < scripts/ccb2008.sql '
              '&& rm scripts/ccb2008.sql', capture=False)
        print(" * removing production-database dump...")
        run('rm %sproject/jetson_project/ccb/tmp/ccb2008.sql' % PRODUCTION_CCB_DIR)
        print
        if env.full or "y" == prompt('Call prepare_dev command (y/n)?', default="y"):
            print(" * preparing data for development...")
            local('cd .. '
                  '&& ./manage.py prepare_dev', capture=False)
            local('cd .. '
                  '&& ./manage.py prepare_dev --settings=settings_icb', capture=False)
    print

    if env.full or "y" == prompt('Download media uploads (y/n)?', default="y"):
        print(" * creating an archive of media uploads...")
        run('cd %sproject/jetson_project/ccb/media/uploads '
            '&& tar -cz --exclude=.svn -f ../../tmp/uploads.tar.gz *'
            % PRODUCTION_CCB_DIR)
        print(" * downloading archive...")
        get("%sproject/jetson_project/ccb/tmp/uploads.tar.gz"
            % PRODUCTION_CCB_DIR,
            "uploads.tar.gz")
        print(" * extracting and removing archive locally...")
        local('cd ../media/uploads/ '
              '&& tar -xzf ../../scripts/uploads.tar.gz '
              '&& rm ../../scripts/uploads.tar.gz', capture=False)
        print(" * removing archive from the server...")
        run("rm %sproject/jetson_project/ccb/tmp/uploads.tar.gz"
            % PRODUCTION_CCB_DIR)
    print

    if env.full or "y" == prompt('Update code (y/n)?', default="y"):
        print(" * updating code...")
        local('cd ../.. && svn up', capture=False)
    print

    if env.full or "y" == prompt('Migrate database schema (y/n)?', default="y"):
        print(" * migrating database schema...")
        local("cd .. && ./manage migrate --no-initial-data", capture=False)
        local("cd .. && ./manage onlysyncdb", capture=False)
    print


def _update_staging():
    """ updates testing environment """
    run("")  # password request
    print

    if env.full or "y" == prompt('Set under-construction screen (y/n)?', default="y"):
        print(" * changing vhost.conf...")
        run('cd %sconf/ '
            '&& cp vhost_under_construction.conf vhost.conf'
            % STAGING_CCB_DIR)
        run('cd %sconf/ '
            '&& cp vhost_under_construction.conf vhost.conf'
            % STAGING_ICB_DIR)
        print(" * restarting apache...")
        run('/etc/init.d/apache2 stop')
        run('/etc/init.d/apache2 start')
    print

    if env.full or "y" == prompt('Get latest production database (y/n)?', default="y"):
        print(" * updating database with production data...")
        run('mysqldump --opt -u ccb2008 -pjkads654 ccb2008 > ccb2008.sql '
            '&& mysql -u test_ccb -ptest123 test_ccb --default-character-set=utf8 < ccb2008.sql '
            '&& rm ccb2008.sql')
        print
        if env.full or "y" == prompt('Call prepare_staging command (y/n)?', default="y"):
            print(" * preparing data for testing...")
            run('cd %s/project/jetson_project/ccb/ '
                '&& ./manage prepare_staging'
                % STAGING_CCB_DIR)
            run('cd %s/project/jetson_project/ccb/ '
                '&& ./manage prepare_staging --settings=settings_icb'
                % STAGING_CCB_DIR)
    print

    if env.full or "y" == prompt('Get latest media uploads (y/n)?', default="y"):
        print(" * updating media uploads...")
        run('cp -R %sproject/jetson_project/ccb/media/uploads/* %sproject/jetson_project/ccb/media/uploads/ '
            '&& chmod -R 0777 %sproject/jetson_project/ccb/media/uploads' % (
                PRODUCTION_CCB_DIR, STAGING_CCB_DIR, STAGING_CCB_DIR))
    print

    if env.full or "y" == prompt('Update code (y/n)?', default="y"):
        print(" * updating code...")
        run('cd %s/project/jetson_project/ccb/ '
            '&& svn up '
            '&& cd ../jetson/'
            '&& svn up'
            % STAGING_CCB_DIR)
    print

    if env.full or "y" == prompt('Migrate database schema (y/n)?', default="y"):
        print(" * migrating database schema...")
        run('cd %s/project/jetson_project/ccb/ '
            '&& ./manage migrate --no-initial-data'
            % STAGING_CCB_DIR)
        run('cd %s/project/jetson_project/ccb/ '
            '&& ./manage onlysyncdb'
            % STAGING_CCB_DIR)
    print

    if env.full or "y" == prompt('Restart memcached (y/n)?', default="y"):
        print(" * restarting memcached...")
        run('/srv/memcached/restart')
    print

    if env.full or "y" == prompt('Unset under-construction screen (y/n)?', default="y"):
        print(" * changing vhost.conf...")
        run('cd %sconf/ '
            '&& cp vhost_live.conf vhost.conf'
            % STAGING_CCB_DIR)
        run('cd %sconf/ '
            '&& cp vhost_live.conf vhost.conf'
            % STAGING_ICB_DIR)
        print(" * restarting apache...")
        run('/etc/init.d/apache2 stop')
        run('/etc/init.d/apache2 start')
    print


def _update_production():
    """ updates production environment """
    if "y" != prompt('Are you sure you want to update production website (y/n)?', default="n"):
        return

    run("")  # password request
    print

    if env.full or "y" == prompt('Set under-construction screen (y/n)?', default="y"):
        print(" * changing vhost.conf...")
        run('cd %sconf/ '
            '&& cp vhost_under_construction.conf vhost.conf'
            % PRODUCTION_CCB_DIR)
        run('cd %sconf/ '
            '&& cp vhost_under_construction.conf vhost.conf'
            % PRODUCTION_ICB_DIR)
        print(" * restarting apache...")
        run('/etc/init.d/apache2 stop')
        run('/etc/init.d/apache2 start')
    print

    if env.full or "y" == prompt('Stop cron jobs (y/n)?', default="y"):
        print(" * stopping cron jobs...")
        run('/etc/init.d/cron stop')
    print

    if env.full or "y" == prompt('Backup database (y/n)?', default="y"):
        print(" * creating a database dump...")
        run('cd %sprivate/ '
            '&& ./backupdb.bsh'
            % PRODUCTION_CCB_DIR)
    print

    if env.full or "y" == prompt('Update code (y/n)?', default="y"):
        print(" * updating code...")
        run('cd %s/project/jetson_project/ccb/ '
            '&& svn up '
            '&& cd ../jetson/'
            '&& svn up'
            % PRODUCTION_CCB_DIR)
    print

    if env.full or "y" == prompt('Change permissions for translation files (y/n)?', default="y"):
        print(" * making translation files writable...")
        run('find %sproject/jetson_project/jetson/locale/ '
            '"(" -name "*.po" -or -name "*.mo" ")" '
            '-exec chmod -R 0666 {} ";"'
            % PRODUCTION_CCB_DIR)
        run('find %sproject/jetson_project/ccb/locale/ '
            '"(" -name "*.po" -or -name "*.mo" ")" '
            '-exec chmod -R 0666 {} ";"'
            % PRODUCTION_CCB_DIR)
    print

    if env.full or "y" == prompt('Migrate database schema (y/n)?', default="y"):
        print(" * migrating database schema...")
        run('cd %s/project/jetson_project/ccb/ '
            '&& ./manage migrate --no-initial-data'
            % PRODUCTION_CCB_DIR)
        run('cd %s/project/jetson_project/ccb/ '
            '&& ./manage onlysyncdb'
            % PRODUCTION_CCB_DIR)
    print

    if env.full or "y" == prompt('Restart memcached (y/n)?', default="y"):
        print(" * restarting memcached...")
        run('/srv/memcached/restart')
    print

    if env.full or "y" == prompt('Start cron jobs (y/n)?', default="y"):
        print(" * starting cron jobs...")
        run('/etc/init.d/cron start')
    print

    if env.full or "y" == prompt('Unset under-construction screen (y/n)?', default="y"):
        print(" * changing vhost.conf...")
        run('cd %sconf/ '
            '&& cp vhost_live.conf vhost.conf'
            % PRODUCTION_CCB_DIR)
        run('cd %sconf/ '
            '&& cp vhost_live.conf vhost.conf'
            % PRODUCTION_ICB_DIR)
        print(" * restarting apache...")
        run('/etc/init.d/apache2 stop')
        run('/etc/init.d/apache2 start')
    print


def deploy():
    """ updates the chosen environment """
    while env.environment not in ("dev", "staging", "production"):
        env.environment = prompt('Please specify target environment ("dev", "staging", or "production"): ')
        print

    globals()["_update_%s" % env.environment]()


def _translate_on_dev():
    run("")  # password request
    print

    if env.full or "y" == prompt('Change permissions for translation files (y/n)?', default="y"):
        print(" * locking files on the production environment...")
        run('find %sproject/jetson_project/jetson/locale/ '
            '"(" -name "*.po" -or -name "*.mo" ")" '
            '-exec chmod -R 0444 {} ";"'
            % PRODUCTION_CCB_DIR)
        run('find %sproject/jetson_project/ccb/locale/ '
            '"(" -name "*.po" -or -name "*.mo" ")" '
            '-exec chmod -R 0444 {} ";"'
            % PRODUCTION_CCB_DIR)
    print

    if env.full or "y" == prompt('Get existing translations (y/n)?', default="y"):
        print(" * commiting from production environment...")
        run('cd %s/project/jetson_project/jetson/locale/ '
            '&& svn commit -m "translations for Jetson"'
            % PRODUCTION_CCB_DIR)
        run('cd %s/project/jetson_project/ccb/locale/ '
            '&& svn commit -m "translations for CCB"'
            % PRODUCTION_CCB_DIR)
        print(" * updating dev environment...")
        local('cd ../../jetson/locale/ '
              '&& svn up', capture=False)
        local('cd ../locale/ '
              '&& svn up', capture=False)
    print

    if env.full or "y" == prompt('Collect translatable strings (y/n)?', default="y"):
        print(" * making messages...")
        local('cd ../../jetson/ '
              '&& django-admin.py makemessages --all && django-admin.py makemessages --all -d djangojs', capture=False)
        local('cd .. '
              '&& django-admin.py makemessages --all && django-admin.py makemessages --all -d djangojs', capture=False)
    print


def _translate_on_production():
    run("")  # password request
    print

    if env.full or "y" == prompt('Compile translations (y/n)?', default="y"):
        print(" * compiling translations in dev environment...")
        local('cd ../../jetson/ '
              '&& django-admin.py compilemessages', capture=False)
        local('cd .. '
              '&& django-admin.py compilemessages', capture=False)
    print

    if env.full or "y" == prompt('Send existing translations to production (y/n)?', default="y"):
        print(" * committing from dev environment...")
        local('cd ../../jetson/locale/ '
              '&& svn commit -m "translations for Jetson"', capture=False)
        local('cd ../locale/ '
              '&& svn commit -m "translations for CCB"', capture=False)
        print(" * updating production environment...")
        run('cd %s/project/jetson_project/jetson/locale/ '
            '&& svn update'
            % PRODUCTION_CCB_DIR)
        run('cd %s/project/jetson_project/ccb/locale/ '
            '&& svn update'
            % PRODUCTION_CCB_DIR)
    print

    if env.full or "y" == prompt('Change permissions for translation files (y/n)?', default="y"):
        print(" * unlocking files on the production environment...")
        run('find %sproject/jetson_project/jetson/locale/ '
            '"(" -name "*.po" -or -name "*.mo" ")" '
            '-exec chmod -R 0666 {} ";"'
            % PRODUCTION_CCB_DIR)
        run('find %sproject/jetson_project/ccb/locale/ '
            '"(" -name "*.po" -or -name "*.mo" ")" '
            '-exec chmod -R 0666 {} ";"'
            % PRODUCTION_CCB_DIR)
    print

    if env.full or "y" == prompt('Restart webserver (y/n)?', default="y"):
        print(" * restarting apache...")
        run('/etc/init.d/apache2 stop')
        run('/etc/init.d/apache2 start')
    print


def translate():
    """ activates translations for the chosen environment """
    while env.environment not in ("dev", "production"):
        env.environment = prompt('Please specify target environment ("dev" or "production"): ')
        print

    globals()["_translate_on_%s" % env.environment]()
