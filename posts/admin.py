from django.contrib import admin
from .models import Post, LikeonPost, CommentonPost
# Register your models here.

admin.site.register(Post)
admin.site.register(LikeonPost)
admin.site.register(CommentonPost)

