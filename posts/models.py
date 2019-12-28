from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from PIL import Image


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='user_posts')
    caption = models.TextField(max_length=1000)
    date = models.DateTimeField(default = now)

    def __str__(self):
        return f'{self.owner.username} - {self.date}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.image.path)


class LikeonPost(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    date = models.DateTimeField(default = now)


class CommentonPost(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField(max_length=200)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    date = models.DateTimeField(default = now)


class LikeonComment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.ForeignKey(CommentonPost, on_delete = models.CASCADE)
    date = models.DateTimeField(default = now)
