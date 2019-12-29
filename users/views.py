from django.contrib.auth.views import LogoutView, LoginView
from .forms import UserRegisterForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post
from django.http import HttpResponseForbidden
from .forms import UserUpdateForm, ProfileUpdateForm


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

    user = get_object_or_404(User, username =  kwargs['username'])
    follower_find = user.profile.followers.all().filter(user = request.user).exists()
    return render(request, 'users/profile.html', {'user': user, 'is_follower' : follower_find})


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






        