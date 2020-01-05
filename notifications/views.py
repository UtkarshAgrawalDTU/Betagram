from django.shortcuts import render
from posts.models import LikeonPost, CommentonPost
from users.models import Request
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def NotifView(request):

    new_notifs = Notification.objects.filter(concerned_user = request.user, date__gte = request.user.time_track.last_login).order_by('-date')
    all_notifs = Notification.objects.filter(concerned_user = request.user, date__lt = request.user.time_track.last_login).order_by('-date')
    request.user.time_track.save()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(all_notifs, 5)    
    
    try:
        old_notifs = paginator.page(page)
    except PageNotAnInteger:
        old_notifs = paginator.page(1)
    except EmptyPage:
        old_notifs = paginator.page(paginator.num_pages)

    return render(request, 'notifications/notifs.html', {'new_notifs': new_notifs, 'old_notifs' : old_notifs})

