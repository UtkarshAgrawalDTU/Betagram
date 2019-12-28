from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from posts.models import Post, LikeonComment, LikeonPost, CommentonPost
from itertools import chain
# Create your views here.

class FeedView(ListView):
    template_name = 'betagram/index.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        profile_following = self.request.user.profile.following.all()
        final = Post.objects.none()
        following = User.objects.filter(profile__in = profile_following)
        final = final.union(Post.objects.filter(owner__in = following))
        return final