from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import *

@receiver(post_save, sender=FriendRequest)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    reciever_ = instance.receiver
    # only if the status has been changed to 'accepted', add friend and save for both users
    if instance.status == 'accepted':
        sender_.friends.add(reciever_.user)
        reciever_.friends.add(sender_.user)
        sender_.save()
        reciever_.save()

@receiver(pre_delete, sender=FriendRequest)
def pre_delete_remove_friend(sender, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    # remove friend on both sides
    sender_.friends.remove(receiver_.user)
    receiver_.friends.remove(sender_.user)
    sender_.save()
    receiver_.save()