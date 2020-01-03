from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from posts.models import Post, LikeonPost, CommentonPost
from itertools import chain
from users.models import Profile
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def FeedView(request):

    if not request.user.is_authenticated:
        return render(request, 'index.html')
    

    profile_following = request.user.profile.following.all()
    posts = Post.objects.filter(owner = request.user)
    following = User.objects.filter(profile__in = profile_following)
    posts_list = posts.union(Post.objects.filter(owner__in = following)).order_by('-date')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts_list, 2)    
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts' : posts}
    return render(request, 'index.html', context)


