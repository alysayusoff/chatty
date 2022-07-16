from pyexpat import model
from attr import fields
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image', 'content', 'created']

class AppUserSerializer(serializers.ModelSerializer):
    user = UserFriendSerializer()
    class Meta:
        model = AppUser
        fields = ['user']

class FriendRequestsRecievedSerialzer(serializers.ModelSerializer):
    sender = AppUserSerializer()
    class Meta:
        model = FriendRequest
        fields = ['sender', 'status']

class FriendRequestsSentSerialzer(serializers.ModelSerializer):
    receiver = AppUserSerializer()
    class Meta:
        model = FriendRequest
        fields = ['receiver', 'status']

class AppUserDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = UserFriendSerializer(many=True)
    posts = PostSerializer(many=True)
    requests_recieved = FriendRequestsRecievedSerialzer(source='reciever', many=True)
    requests_sent = FriendRequestsSentSerialzer(source='sender', many=True)
    class Meta:
        model = AppUser
        fields = [
            'user', 
            'first_name', 
            'last_name', 
            'pfp', 
            'posts', 
            'friends', 
            'requests_recieved', 
            'requests_sent'
        ]