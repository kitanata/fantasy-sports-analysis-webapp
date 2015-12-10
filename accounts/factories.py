import factory
import factory.django
from . import models


class EmailUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EmailUser

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
