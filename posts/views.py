from django.shortcuts import render
from django.views.generic import DetailView
from .models import Post
# Create your views here.


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    
