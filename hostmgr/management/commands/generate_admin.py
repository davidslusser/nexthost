from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.conf import settings
from jinja2 import Template
import os

__version__ = "0.0.1"


class Command(BaseCommand):
    help = "Generate admin.py file, based on a jinja2 template, for a given app"

    def __inti__(self):
        self.app = None
        self.model_list = None
        super(Command, self).__init__()

    def add_arguments(self, parser):
        """ define command arguments """
        parser.add_argument('app', type=str, help='enter the name of the django app')
        parser.add_argument('--admin_template', type=str, help='path to Jinja template used to create admin.py file')

    def handle(self, *args, **options):
        """ command entry point """
        if options['app'] not in settings.INSTALLED_APPS:
            raise CommandError("'{}' is not an available application in this project".format(options['app']))

        self.app = options['app']
        self.model_list = self.get_model_list()

        self.build_admin()

        self.stdout.write(self.style.SUCCESS('admin.py generated!'))

    def get_model_list(self):
        """ return a list of all models in application """
        app = apps.get_app_config(self.app)
        return list(app.get_models())

    @staticmethod
    def get_model_field_names(model, exclude_list=()):
        """ return a list of field names for a given model """
        return [i.name for i in model._meta.fields if type(i).__name__ not in exclude_list]

    def build_admin(self, output_file=None, template_file=None):
        """ build the admin.py file """
        model_fields = {}
        for model in self.model_list:
            model_fields[model.__name__] = self.get_model_field_names(model)

        if not template_file:
            template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates", "admin.jinja")

        if not output_file:
            output_file = "admin_tmp.py"

        data = {"model_list": self.model_list,
                "app_name": self.app,
                "models_file": "models",
                # "model_fields": model_fields,
                "model_data": self.get_models_and_fields(),
                }

        with open(template_file) as f:
            template = Template(f.read())
        file_text = template.render(data)

        with open(output_file, "w") as f:
            f.write(file_text)

        print("COMMAND completed!")

    @staticmethod
    def get_display_fields(model):
        """ build and return a list of 'display_fields' to be used in admin.py for a given model """
        exclude_list = ['AutoField']
        return [i.name for i in model._meta.fields if i.get_internal_type() not in exclude_list]

    @staticmethod
    def get_search_fields(model):
        """ build and return a list of 'search_fields' to be used in admin.py for a given model """
        exclude_list = ['AutoField', 'BooleanField', 'DateTimeField', 'ForeignKey']
        return [i.name for i in model._meta.fields if i.get_internal_type() not in exclude_list]

    def get_models_and_fields(self):
        return_data = {}
        for model in self.model_list:
            return_data[model.__name__] = {'display_fields': self.get_display_fields(model),
                                           'search_fields': self.get_search_fields(model),
                                           }
        print(return_data)
        return return_data
