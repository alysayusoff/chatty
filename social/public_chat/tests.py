from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class ChatTest(TestCase):
    good_url = ''
    bad_url = ''   

    def setUp(self):
        # good url will reverse user-api with keyword argument room_name as testlobby
        self.good_url = reverse('room', kwargs={'room_name' : 'testlobby'})
        # invalid url
        self.bad_url = 'chat/10'

    def test_ChatReturnSuccess(self):
        # get response from url
        response = self.client.get(self.good_url)
        # check 
        self.assertEqual(response.status_code, 302)
        
    def test_ChatReturnFailure(self):
        # get response from url
        response = self.client.get(self.bad_url)
        # check if failed
        self.assertEqual(response.status_code, 404)