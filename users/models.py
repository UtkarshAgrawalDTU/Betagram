from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.timezone import now


class Profile(models.Model):

    #One and only one
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') 
    bio = models.TextField(default="", max_length=100)
    image = models.ImageField(upload_to='user_profile_pic', default='default.jpg') 
    following = models.ManyToManyField("self", symmetrical=False, related_name='followers', blank = True)


    def __str__(self):
        return f'{self.user.username} - Profile'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Request(models.Model):

    follower_req = models.ForeignKey(User, on_delete = models.CASCADE, related_name='requests_by_me')
    following_req = models.ForeignKey(User, on_delete = models.CASCADE, related_name='requests_for_me')
    date = models.DateTimeField(default = now)

    class Meta:
        unique_together = ('follower_req', 'following_req',)

    def __str__(self):
        return f'{self.follower_req.username} ---> {self.following_req.username}'
    

class TimeTrack(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='time_track')
    last_login = models.DateTimeField(default = now)

    def __str__(self):
        return f'Last login by {self.user.username} at {self.last_login}'

    def save(self, *args, **kwargs):
        self.last_login = now()
        super().save(*args, **kwargs)
        