from django.shortcuts import render
from posts.models import LikeonPost, CommentonPost
from users.models import Request
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def NotifView(request):

    new_notifs = Notification.objects.filter(concerned_user = request.user, date__gte = request.user.time_track.last_login).order_by('-date')
    all_notifs = Notification.objects.filter(concerned_user = request.user, date__lt = request.user.time_track.last_login).order_by('-date')
    request.user.time_track.save()
    return render(request, 'notifications/notifs.html', {'new_notifs': new_notifs, 'all_notifs' : all_notifs})

