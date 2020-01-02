from django.shortcuts import render
from posts.models import LikeonPost, CommentonPost
from users.models import Request
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Notification

class NotifView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notifs.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        object_list = Notification.objects.filter(concerned_user = self.request.user).order_by('-date')
        return object_list

