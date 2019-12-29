from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from posts.models import Post, LikeonComment, LikeonPost, CommentonPost
from itertools import chain
from users.models import Profile
from django.shortcuts import redirect
# Create your views here.

def FeedView(request):

    if not request.user.is_authenticated:
        return render(request, 'betagram/index.html')

    profile_following = request.user.profile.following.all()
    posts = Post.objects.filter(owner = request.user)
    following = User.objects.filter(profile__in = profile_following)
    posts = posts.union(Post.objects.filter(owner__in = following)).order_by('-date')
    context = {'all_posts' : posts}
    return render(request, 'betagram/index.html', context)


