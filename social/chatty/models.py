from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image

class AppUser(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pfp = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.user.username}"

    # returns all user's friends
    def get_friends(self):
        return self.friends.all()

    # returns number of friends
    def get_number_of_friends(self):
        return self.friends.all().count()

    # returns number of posts posted by user
    def get_number_of_posts(self):
        return self.posts.all().count()

    # returns all posts posted by user
    def get_posts(self):
        return self.posts.all()
        
    def save(self, *args, **kwargs):
        super(AppUser, self).save(*args, **kwargs)
        img = Image.open(self.pfp.path)
        if img.height > 150:
            height = 150
            width = img.width * (img.height / height)
            output_size = (width, height)
            img.thumbnail(output_size)
            img.save(self.pfp.path)

STATUS = (
    ('sent', 'sent'),
    ('accepted', 'accepted')
)

class FriendRequest(models.Model):
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='reciever')
    status = models.CharField(max_length=8, choices=STATUS)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
    
    # returns the sender's username
    def get_sender(self):
        return f"{self.sender}"

class Post(models.Model):
    content = models.TextField(max_length=200, null=False)
    image = models.ImageField(
        upload_to='posts/', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])], blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content)

    # returns the date the post was created
    def get_created(self):
        return str(self.created.strftime("%d-%m-%Y %H:%M"))

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.width > 150:
                width = 150
                height = img.height * (img.width / width)
                output_size = (width, height)
                img.thumbnail(output_size)
                img.save(self.image.path)

    # order the posts in reverse of when it was created
    class Meta:
        ordering = ('-created',)