import pprint
import random

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.utils import IntegrityError
from faker.factory import Factory

# Create a localized instance of Faker for Italian locale
fake = Factory.create('it_IT')
# Create a localized instance of Faker for Italian locale
pp = pprint.PrettyPrinter()


def get_models_from_app(app_name):
    app_config = apps.get_app_config(app_name)
    # Get a list of all model classes registered in the application
    model_classes = app_config.get_models()
    # Print the names of the model classes
    for model_class in model_classes:
        print(model_class.__name__, sep='', end=',')
    return model_classes


def get_all_apps():
    installed_apps = settings.INSTALLED_APPS
    names = []
    for app_name in installed_apps:
        names.append(app_name)
    return names


def fake_charfield(field) -> str:
    """Generates fake data for a charfield based on its name. Returns Lorem Ipsum text if no matches"""
    fname = field.name.lower()
    if 'surame' in fname:
        return fake.last_name()
    elif 'first_name' in fname:
        return fake.first_name()
    elif 'last_name' in fname:
        return fake.first_name()
    elif 'address' in fname:
        return fake.street_address()
    elif 'cap' in fname:
        return fake.postcode()
    elif 'city' in fname:
        return fake.city()
    elif 'value' in fname:
        return fake.sentence(nb_words=2)
    elif 'mobile' in fname:
        return fake.phone_number()
    elif 'telephone' in fname:
        return fake.phone_number()
    elif 'phone' in fname:
        return fake.phone_number()
    elif 'tax_number' in fname:
        return fake.ssn()
    elif 'vat_number' in fname:
        return fake.company_vat()
    elif 'coordinates' in fname:
        ll = fake.local_latlng(country_code='IT')
        return f"{ll[0]}, {ll[1]}"
    else:
        return fake.word()


def generate_fake_data(field):
    """Generates fake data for the field based on its type"""
    if isinstance(field, models.CharField):
        return fake_charfield(field)
    elif isinstance(field, models.IntegerField) or isinstance(field, models.PositiveIntegerField):
        return random.randint(0, 100)
    elif isinstance(field, models.FloatField):
        return random.uniform(0, 100)
    elif isinstance(field, models.DateField):
        return fake.date_this_year()
    elif isinstance(field, models.DateTimeField):
        return fake.date_time_this_year()
    elif isinstance(field, models.BooleanField):
        return fake.boolean()
    elif isinstance(field, models.EmailField):
        return fake.email()
    elif isinstance(field, models.URLField):
        return fake.url()
    elif isinstance(field, models.ForeignKey) or isinstance(field, models.OneToOneField):
        related_model = field.related_model
        created, related_instance = create_fake_instance(related_model)
        if related_instance:
            return related_instance
    # Add more field type checks and corresponding fake data generation here
    else:
        return None


def clean_field_list(fields):
    """Cleans meta or autogenerated fields from autogenerated fields"""
    for field in fields.copy():
        if field.name == 'deleted_at':
            fields.remove(field)
        elif field.name == 'id':
            fields.remove(field)
        elif field.name == 'created_at':
            fields.remove(field)
    return fields


def create_fake_instance(model_class):
    """Creates a fake instance of the given model"""
    fields = model_class._meta.fields  # Gets the fields
    fake_instance_data = {}
    my_fields = list(fields)
    print(f"Preparing to fill {model_class}")
    print(f"Fields found: {my_fields}")
    my_fields = clean_field_list(my_fields)
    for field in my_fields:
        # generates a dict of data
        fake_value = generate_fake_data(field)
        if fake_value is not None:
            fake_instance_data[field.name] = fake_value
    print("---------- Data going to be saved: --------------")
    pp.pprint(fake_instance_data)
    try:
        fake_instance = model_class.objects.create(**fake_instance_data)
    except IntegrityError:
        try:
            fake_instance_data['username'] = fake.user_name()
            fake_instance = model_class.objects.create(**fake_instance_data)
        except IntegrityError:
            fake_instance_data['username'] = fake.user_name()
            fake_instance = model_class.objects.create(**fake_instance_data)

    fake_instance.save()
    if fake_instance:
        return True, fake_instance


class Command(BaseCommand):
    help = 'Import Master Tables'

    def handle(self, *args, **options):

        print("ciao tommaso")