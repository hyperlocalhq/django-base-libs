from django.apps import AppConfig


class BaseLibsConfig(AppConfig):
    name = "base_libs.apps.base_libs_app"
    verbose_name = "Base Libs"

    def ready(self):
        import base_libs.utils.django_cms
