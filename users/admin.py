from django.contrib import admin
from .models import Profile, Request, TimeTrack


admin.site.register(Profile)
admin.site.register(Request)
admin.site.register(TimeTrack)