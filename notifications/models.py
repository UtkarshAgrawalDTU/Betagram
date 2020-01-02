from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from django.utils.timezone import now
from posts.models import Post
# Create your models here.


class Notification(models.Model):
    date = models.DateTimeField(default = now)
    concerned_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='notification')
    action_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='action_user')
    notification_type = models.CharField(max_length=10)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='history', blank = True, null = True)

    def __str__(self):
        return f'{self.action_user} {self.notification_type} {self.concerned_user}'
    
