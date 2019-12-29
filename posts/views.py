from django.shortcuts import render
from django.views.generic import DetailView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


class PostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        follower_find = post.owner.profile.followers.all().filter(user = self.request.user)
        if self.request.user == post.owner or follower_find.exists() :
            return True
        return False
    
