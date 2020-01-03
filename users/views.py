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
from notifications.models import Notification
from django.contrib.auth import views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def RequestView(request, **kwargs):

    if request.method == 'POST':

        follower = User.objects.get(username = request.POST['follower'])
        status = request.POST['status']

        if status == 'accept':
            request.user.profile.followers.add(follower.profile)
            Request.objects.get(follower_req = follower, following_req = request.user).delete()
            Notification.objects.create(concernced_user = follower, action_user = request.user, notification_type = 'req_accept')

        if status == 'reject':
            Request.objects.get(follower_req = follower, following_req = request.user).delete()

    object_list = request.user.requests_for_me.all().order_by('-date')

    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 10)    
    
    try:
        requests = paginator.page(page)
    except PageNotAnInteger:
        requests = paginator.page(1)
    except EmptyPage:
        requests = paginator.page(paginator.num_pages)

    return render(request, 'users/requests.html', {'requests': requests})


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

        if status == 'accept':
            request.user.profile.followers.add(prof_user.profile)
            Request.objects.get(follower_req = prof_user, following_req = request.user).delete()
            Notification.objects.create(concerned_user = prof_user, action_user = request.user, notification_type = 'req_accept')


        if status == 'reject':
            Request.objects.get(follower_req = prof_user, following_req = request.user).delete()


        if status == 'follow':
            Request.objects.create(follower_req = request.user, following_req = prof_user)
            Notification.objects.create(concerned_user = prof_user, action_user = request.user, notification_type = 'request')


        if status == 'unfollow':
            request.user.profile.following.remove(prof_user.profile)


        if status == 'unfollowed':
            request.user.profile.followers.remove(prof_user.profile)


        if status == 'remove_request':
            Request.objects.filter(follower_req = request.user, following_req = prof_user).delete()
            Notification.objects.filter(concerned_user = prof_user, action_user = request.user, notification_type = 'request').delete()


    posts_set = Post.objects.filter(owner = request.user).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts_set, 20)    
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    is_following = request.user.profile.following.all().filter(user = prof_user).exists()
    is_followed = request.user.profile.followers.all().filter(user = prof_user).exists()
    request_sent = Request.objects.filter(follower_req = request.user, following_req = prof_user).exists()
    accept_req = Request.objects.filter(follower_req = prof_user, following_req = request.user).exists()
    return render(request, 'users/profile.html', {'user': prof_user, 'is_following' : is_following, 'is_followed' : is_followed, 'request_sent' : request_sent, 'accept_request' : accept_req, 'posts':posts})






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



class PasswordResetView(views.PasswordResetView):
    template_name = 'users/password_reset.html'

class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'

class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
