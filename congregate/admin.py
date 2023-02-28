from django.contrib import admin
from .models import User, Group, Event, Activity, Vote
# Register your models here.

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Event)
admin.site.register(Activity)
admin.site.register(Vote)
