import factory
import factory.django
import factory.fuzzy
from wagtail.wagtaildocs.models import Document


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    title = factory.Sequence(lambda n: 'Document {}'.format(n))
    file = factory.django.FileField(filename='somepdf.pdf')
