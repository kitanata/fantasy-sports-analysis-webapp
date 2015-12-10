import factory
import factory.django
import factory.fuzzy
from django.utils import timezone
from django.utils.text import slugify
from accounts.factories import EmailUserFactory
from . import models


class SportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Sport

    name = factory.Sequence(lambda n: 'Sport {}'.format(n))


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Sequence(lambda n: 'Product {}'.format(n))
    recurly_plan_code = factory.LazyAttribute(
        lambda obj: '{}'.format(slugify(obj.name)[:50])
    )
    duration = factory.Iterator([models.Product.DAILY, models.Product.MONTHLY])
    sport = factory.SubFactory(SportFactory)
    price = factory.fuzzy.FuzzyDecimal(200)


class LineUpFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.LineUp

    pdf = factory.django.FileField(filename='somepdf.pdf')
    date_uploaded = factory.LazyAttribute(lambda obj: timezone.now())

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of products were passed in, use them
            for product in extracted:
                self.products.add(product)


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Subscription

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(EmailUserFactory)
    uuid = factory.Sequence(lambda n: n)
    state = models.Subscription.ACTIVE
    activated_at = factory.LazyAttribute(lambda obj: timezone.now())


class UserWithSubscriptionFactory(EmailUserFactory):
    membership = factory.RelatedFactory(SubscriptionFactory, 'user')
