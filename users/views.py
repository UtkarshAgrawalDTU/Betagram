from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import ListView
from posts.models import Post
from .models import Request
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


@login_required
def RequestView(request, **kwargs):

    if request.method == 'POST':

        follower = User.objects.get(username = request.POST['follower'])
        status = request.POST['status']

        if status == 'accept':
            request.user.profile.followers.add(follower.profile)
            Request.objects.get(follower_req = follower, following_req = request.user).delete()

        if status == 'reject':
            Request.objects.get(follower_req = follower, following_req = request.user).delete()

    object_list = request.user.requests_for_me.all().order_by('-date')
    return render(request, 'users/requests.html', {'requests': object_list})


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'betagram/index.html'


def UserRegisterView(request, *args, **kwargs):

    if request.user.is_authenticated:
        return redirect('feed:home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created. You can now login !')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})





@login_required
def ProfileView(request, **kwargs):

    prof_user = get_object_or_404(User, username =  kwargs['username'])
    
    if request.method == 'POST':

        status = request.POST['status']

        if status == 'follow':
            Request.objects.create(follower_req = request.user, following_req = prof_user)

        if status == 'unfollow':
            request.user.profile.following.remove(prof_user.profile)

        if status == 'unfollowed':
            request.user.profile.followers.remove(prof_user.profile)
        
        if status == 'remove_request':
            Request.objects.filter(follower_req = request.user, following_req = prof_user).delete()

    is_following = request.user.profile.following.all().filter(user = prof_user).exists()
    is_followed = request.user.profile.followers.all().filter(user = prof_user).exists()
    request_sent = Request.objects.filter(follower_req = request.user, following_req = prof_user).exists()

    return render(request, 'users/profile.html', {'user': prof_user, 'is_following' : is_following, 'is_followed' : is_followed, 'request_sent' : request_sent})






@login_required
def EditProfileView(request, **kwargs):

    user = get_object_or_404(User, username =  kwargs['username'])
    
    if not request.user.is_authenticated or not request.user == user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated !')
            return redirect('profile', username = user.username)
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance= request.user.profile)

    context = {'u_form' : u_form, 'p_form' : p_form, 'user' : user}
    return render(request, 'users/profile_form.html', context)



@login_required
def FollowerListView(request, **kwargs):
    
    user = get_object_or_404(User, username = kwargs['username'])
    
    if not request.user.profile.following.filter(user = user).exists() and not request.user == user:
        return HttpResponseForbidden()
    
    object_list = user.profile.followers.all()

    if request.method == 'POST':

        follower = User.objects.get(username = request.POST['follower'])
        status = request.POST['status']
        
        if status == 'unfollowed':
            user.profile.followers.remove(follower.profile)

    return render(request, 'users/follower_list.html', {'followers': object_list})



@login_required
def FollowingListView(request, **kwargs):
    
    user = get_object_or_404(User, username = kwargs['username'])
    
    if not request.user.profile.following.filter(user = user).exists() and not request.user == user:
        return HttpResponseForbidden()

    object_list = user.profile.following.all()

    if request.method == 'POST':

        following = User.objects.get(username = request.POST['following'])
        status = request.POST['status']
        
        if status == 'unfollow':
            user.profile.following.remove(following.profile)

    return render(request, 'users/following_list.html', {'following_list': object_list})


        