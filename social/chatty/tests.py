from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from .model_factories import *
from .serializers import *
from .api import *
from .forms import *

class UserTest(TestCase):
    user = None
    bad_user = None

    def setUp(self):
        # create user
        self.user = UserFactory.create(username='UserTest')

    def tearDown(self):
        User.objects.all().delete()

    def test_UserCreated(self):
        # get user
        created = User.objects.get(pk = self.user.pk)
        # check if user has been created (True)
        self.assertTrue(created)

    def test_UserCreatedWithCorrectData(self):
        # check all values match
        self.assertEqual(self.user.username, 'UserTest')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.password, 'password')

class AppUserTest(TestCase):
    user = None
    appuser = None

    def setUp(self):
        # create user
        self.user = UserFactory.create(username='AppUserTest')
        # create appuser and assign user instance
        self.appuser = AppUserFactory.create(user=self.user)
    
    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
    
    def test_AppUserCreated(self):
        # get user
        created = AppUser.objects.get(pk = self.appuser.pk)
        # check if appuser has been created (True)
        self.assertTrue(created)

    def test_AppUserCreatedWithCorrectData(self):
        # check all values match
        self.assertEqual(self.appuser.user, self.user)
        self.assertEqual(self.appuser.first_name, 'Jane')
        self.assertEqual(self.appuser.last_name, 'Doe')
        self.assertEqual(self.appuser.pfp, 'profile_pics/default.png')

class FriendRequestTest(TestCase):
    user1 = None
    user2 = None
    appuser1 = None
    appuser2 = None
    friendrequest1 = None

    def setUp(self):
        self.user1 = UserFactory.create(username='FriendRequestTest1')
        self.user2 = UserFactory.create(username='FriendRequestTest2')
        self.appuser1 = AppUserFactory.create(user=self.user1)
        self.appuser2 = AppUserFactory.create(user=self.user2)
        # create friendrequest and assign corresponding fields
        self.friendrequest1 = FriendRequestFactory.create(sender=self.appuser1, receiver=self.appuser2)
    
    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        FriendRequest.objects.all().delete()

    def test_FriendRequestCreated(self):
        # get friendrequest
        created = FriendRequest.objects.get(pk = self.friendrequest1.pk)
        self.assertTrue(created)

    def test_FriendRequestCreatedWithCorrectData(self):
        # check if all values match
        self.assertEqual(self.friendrequest1.sender.user, self.user1)
        self.assertEqual(self.friendrequest1.sender, self.appuser1)
        self.assertEqual(self.friendrequest1.receiver.user, self.user2)
        self.assertEqual(self.friendrequest1.receiver, self.appuser2)
        self.assertEqual(self.friendrequest1.status, 'sent')

class PostTest(TestCase):
    user = None
    appuser = None
    post = None

    def setUp(self):
        self.user = UserFactory.create(username='AppUserTest')
        self.appuser = AppUserFactory.create(user=self.user)
        # create post and assign appuser instance
        self.post = PostFactory.create(author=self.appuser)
    
    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Post.objects.all().delete()
    
    def test_PostCreated(self):
        # get post 
        created = Post.objects.get(pk = self.post.pk)
        self.assertTrue(created)

    def test_PostCreatedWithCorrectData(self):
        # check all values match
        self.assertEqual(self.post.author.user, self.user)
        self.assertEqual(self.post.author, self.appuser)
        self.assertEqual(self.post.content, 'post')
        self.assertEqual(self.post.image, 'posts/Picnic-buzzket.jpg')

class UserFormTest(TestCase):
    good_form = None
    bad_form = None
    invalid_form = None

    def setUp(self):
        # good form will have all valid inputs
        self.good_form = UserForm(data={
            'username' : 'UserFormTest',
            'email' : 'UserFormTest@example.com',
            'password' : 'password'
        })
        # invalid form will have one invalid input, email
        self.invalid_form = UserForm(data={
            'username' : 'UserFormTest',
            'email' : 'UserFormTest',
            'password' : 'password'
        })
        # bad form all empty input
        self.bad_form = UserForm(data={})

    def test_UserFormValid(self):
        # check if form is valid
        self.assertTrue(self.good_form.is_valid())
        # check if form has no errors
        self.assertEqual(self.good_form.errors, {})
    
    def test_UserFormInvalid(self):
        # check if form is invalid
        self.assertFalse(self.bad_form.is_valid())

    def test_UserFormInvalidEmail(self):
        # check for email error
        self.assertEqual(self.invalid_form.errors['email'], ['Enter a valid email address.'])

class UserProfileFormTest(TestCase):
    good_form = None
    bad_form = None

    def setUp(self):
        self.good_form = UserProfileForm(data={
            'first_name' : 'UserProfileFormTest',
            'last_name' : 'UserProfileFormTest'
        })
        self.bad_form = UserProfileForm(data={})

    def test_UserProfileFormValid(self):
        self.assertTrue(self.good_form.is_valid())
        self.assertEqual(self.good_form.errors, {})

    def test_UserProfileFormInvalid(self):
        self.assertFalse(self.bad_form.is_valid())

class PostFormTest(TestCase):
    good_form = None
    bad_form = None

    def setUp(self):
        self.good_form = PostForm(data={
            'content' : 'UserProfileFormTest',
            'pfp' : 'posts/Picnic-buzzket.jpg'
        })
        self.bad_form = PostForm(data={})

    def test_UserProfileFormValid(self):
        self.assertTrue(self.good_form.is_valid())
        self.assertEqual(self.good_form.errors, {})

    def test_UserProfileFormInvalid(self):
        self.assertEqual(self.bad_form.errors['content'], ['This field is required.'])
        self.assertFalse(self.bad_form.is_valid())

class AppUserDetailsSerializerTest(APITestCase):
    user = None
    appuser = None
    appuserserializer = None
    good_url = ''
    bad_url = ''

    def setUp(self):
        self.user = UserFactory.create(username='AppUserDetailsSerializerTest')
        self.appuser = AppUserFactory.create(user=self.user)
        # create appuserserializer and assign appuser instance
        self.appuserserializer = AppUserDetailsSerializer(instance=self.appuser)
        # good url will reverse user-api with keyword argument pk as 1
        self.good_url = reverse('user-api', kwargs={'pk' : 1})
        # invalid url
        self.bad_url = 'api/user/q1'

    def tearDown(self):
        User.objects.all().delete()

    def test_AppUserDetailsSerializer(self):
        # get data from serializer
        data = self.appuserserializer.data
        # check if data fields are as expected
        self.assertEqual(set(data.keys()), set(['user', 'first_name', 'last_name', 'pfp', 'posts', 'friends', 
        'requests_recieved', 'requests_sent']))

    def test_AppUserDetailsSerializerReturnSuccess(self):
        # get response from url
        response = self.client.get(self.good_url)
        # check 
        self.assertEqual(response.status_code, 302)
        
    def test_AppUserDetailsSerializerReturnFailure(self):
        # get response from url
        response = self.client.get(self.bad_url)
        # check if failed
        self.assertEqual(response.status_code, 404)