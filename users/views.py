from django.contrib.auth.views import LogoutView, LoginView
from .forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages

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