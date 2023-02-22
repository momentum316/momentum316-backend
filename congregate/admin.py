from django.contrib import admin
from .models import User, CongregateUser, Group, Event, EventOption
# Register your models here.

admin.site.register(User)
admin.site.register(CongregateUser)
admin.site.register(Group)
admin.site.register(Event)
admin.site.register(EventOption)
