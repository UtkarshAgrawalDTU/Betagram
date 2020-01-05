from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Profile
from django.contrib.auth.models import User
from django.db.models import Q


class SearchResultView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'search/search_results.html'
    context_object_name = 'user'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query == "":
            return User.objects.none()
        object_list = User.objects.filter(
            Q(username__icontains = query) | Q(first_name__icontains = query) | Q(last_name__icontains = query) | Q(email__icontains = query)
        )[:10]
        return object_list

