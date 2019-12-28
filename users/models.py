from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

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


