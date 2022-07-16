from datetime import datetime
import factory
from .models import *

class UserFactory(factory.django.DjangoModelFactory):
    username = 'test'
    email = 'test@example.com'
    password = 'password'

    class Meta:
        model = User

class AppUserFactory(factory.django.DjangoModelFactory):
    first_name = 'Jane'
    last_name = 'Doe'
    user = factory.SubFactory(UserFactory)
    pfp = 'profile_pics/default.png'

    class Meta:
        model = AppUser

class FriendRequestFactory(factory.django.DjangoModelFactory):
    sender = factory.SubFactory(AppUserFactory)
    receiver = factory.SubFactory(AppUserFactory)
    status = 'sent'

    class Meta:
        model = FriendRequest

class PostFactory(factory.django.DjangoModelFactory):
    content = 'post'
    image = 'posts/Picnic-buzzket.jpg'
    author = factory.SubFactory(AppUserFactory)

    class Meta:
        model = Post

# class PostFactory(factory.django.DjangoModelFactory):
#     content = 'post'
#     image = 'posts/Picnic-buzzket.jpg'
#     created = datetime.now().astimezone()
#     author = factory.SubFactory(AppUserFactory)

#     class Meta:
#         model = Post