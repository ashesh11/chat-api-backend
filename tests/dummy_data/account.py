import factory
from account.models.account import UserAccount

class EmailSignupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAccount

    id = 1
    email = 'test@test.com'
    password = 'test'