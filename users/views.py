from django.contrib.auth.views import LogoutView, LoginView


class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    template_name = 'betagram/index.html'