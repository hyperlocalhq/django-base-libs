# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    SILENT, NORMAL, VERBOSE, VERY_VERBOSE = 0, 1, 2, 3
    help = "Switches plain text to rich text for all models."

    def handle(self, *args, **options):
        from django.apps import apps
        from base_libs.models.base_libs_settings import (
            MARKUP_HTML_WYSIWYG,
            MARKUP_PLAIN_TEXT,
            MARKUP_MARKDOWN,
        )

        self.verbosity = int(options.get("verbosity", self.NORMAL))

        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"=== Switching from plain text to rich text ===\n")

        total_counter = 0
        for model in apps.get_models():
            fields_with_markup_types = []
            for field in model._meta.get_fields():
                if field.name.endswith("_markup_type"):
                    fields_with_markup_types.append(
                        field.name.replace("_markup_type", "")
                    )
            if fields_with_markup_types:
                if self.verbosity >= self.NORMAL:
                    self.stdout.write(
                        "{model_name}: {fields_with_markup_types}\n".format(
                            model_name=model.__name__,
                            fields_with_markup_types=", ".join(
                                fields_with_markup_types
                            ),
                        )
                    )
                    self.stdout.flush()
                counter = 0
                for instance in model._default_manager.all():
                    new_values = {}
                    for field_name in fields_with_markup_types:
                        if getattr(instance, "{}_markup_type".format(field_name)) in (
                            MARKUP_PLAIN_TEXT,
                            MARKUP_MARKDOWN,
                        ):
                            new_values[field_name] = getattr(
                                instance, "get_rendered_{}".format(field_name)
                            )()
                            new_values[
                                "{}_markup_type".format(field_name)
                            ] = MARKUP_HTML_WYSIWYG
                    if new_values:
                        model._default_manager.filter(pk=instance.pk).update(
                            **new_values
                        )
                        counter += 1
                if self.verbosity >= self.NORMAL:
                    self.stdout.write(
                        "Instances updated for {model_name}: {counter}\n".format(
                            model_name=model.__name__, counter=counter
                        )
                    )
                    self.stdout.flush()
                total_counter += counter
        if self.verbosity >= self.NORMAL:
            self.stdout.write(u"-----------------------------------------------------\n")
            self.stdout.write(u"Total instances changed: {}\n".format(total_counter))
