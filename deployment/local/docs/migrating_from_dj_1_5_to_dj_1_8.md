# Migrating from Django 1.5 to Django 1.8

Have two project instances side by side: one for __master__ branch and one for __django_1_8__ branch.

## 1. Working with the project using the __master__ branch

1. Download the MySQL database dump from the production server.

2. Import the dump into the local MySQL database.

3. Run __export_cms_pages.sh__.

4. Copy file __cms_pages.json__ from __master__-branch project to __django_1_8__-branch project.

5. Run __remove_cms_from_db.sh__.

6. Export the local MySQL database dump from the __master__-branch project and import to local MySQL database 
in the __django_1_8__-branch project.

## 2. Working with the project using the __django_1_8__ branch

1. Run __apply_django_1_8_migrations.sh__.

2. Make a local MySQL database dump as a backup.

3. Run __import_cms_pages_and_plugins.py__.

4. Run __python tests/django_functional_tests.py__.

5. Switch the settings to use PostgreSQL instead of MySQL.

6. Create PostgreSQL user.

7. (Re)create PostgreSQL database.

8. Run __python manage.py migrate__.

9. Run __convert_db.sh__.

10. Run __python tests/django_functional_tests.py__.

# 3. Arrange the branches

1. Tag the __master__ branch as __django_1_5__.

2. Merge the __django_1_8__ branch to __master__.

