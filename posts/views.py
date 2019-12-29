from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
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
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'caption']
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user     
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['image', 'caption']
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        
        form.instance.owner = self.request.user     
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/post_delete_confirm.html'
    success_url = '/'

    def  test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False

