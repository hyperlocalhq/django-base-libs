# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from optparse import make_option

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    help = """Checks and informs about the dependencies of the installed apps"""

    def handle_noargs(self, **options):

        from django.conf import settings

        from base_libs.utils.misc import is_installed, get_installed
        from base_libs.utils.console import colored
        from jetson.dependencies import APP_DEPENDENCIES as DEPS

        # collecting installed apps
        installed = dict(
            [
                (app.split(".")[-1], {
                    'path': app
                }) for app in settings.INSTALLED_APPS if not app.endswith(".*")
            ]
        )

        # collecting dependencies
        for app in installed:
            installed[app]['used_by'] = []
            installed[app]['using'] = {}
            installed[app]['can_use'] = {}
            if is_installed(app + ".dependencies.required_apps"):
                installed[app]['required_apps'] = get_installed(
                    "%s.dependencies.required_apps" % app,
                )
                installed[app]['optional_apps'] = get_installed(
                    "%s.dependencies.optional_apps" % app,
                )
            elif app in DEPS:
                installed[app]['required_apps'] = DEPS[app]['required_apps']
                installed[app]['optional_apps'] = DEPS[app]['optional_apps']

        # checking dependencies
        for app in installed:
            if "required_apps" in installed[app]:
                for dep in installed[app]['required_apps']:
                    ok = is_installed("%s.models" % dep)
                    installed[app]['using'][dep] = ok
                    if ok:
                        installed[dep]['used_by'].append(app)
                for dep in installed[app]['optional_apps']:
                    ok = is_installed("%s.models" % dep)
                    installed[app]['can_use'][dep] = ok
                    if ok:
                        installed[dep]['used_by'].append(app)

        # report results
        for app in settings.INSTALLED_APPS:
            if app.endswith(".*"):
                continue
            app_info = installed[app.split(".")[-1]]
            print colored(app_info['path'], "yellow")

            if app_info['used_by']:
                print "    used by:"
                for dep in sorted(app_info['used_by']):
                    print "        ", colored(dep, "white")

            if app_info['using']:
                print "    needs:"
                for dep in sorted(app_info['using'].keys()):
                    print "        ", colored(dep, "white"), (
                        app_info['using'][dep] and " " or
                        colored("NOT INSTALLED", "red")
                    )

            if app_info['can_use']:
                print "    optionally uses:"
                for dep in sorted(app_info['can_use'].keys()):
                    print "        ", colored(dep, "white"), (
                        app_info['can_use'][dep] and " " or
                        colored("not installed", "red")
                    )

            if not app_info['used_by'] and not app_info[
                'using'] and not app_info['can_use']:
                print "    no dependencies"
