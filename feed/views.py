from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from posts.models import Post, LikeonComment, LikeonPost, CommentonPost
# Create your views here.

class FeedView(ListView):
    template_name = 'minigram/index.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        
        Post = []
        for follower in followers:
            Post += Post.objects.filter(onwer = follower)
        return Post