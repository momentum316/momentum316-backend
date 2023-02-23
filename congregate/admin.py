from django.contrib import admin
from .models import User, CongregateUser, Group, Event, Activity
# Register your models here.

admin.site.register(User)
admin.site.register(CongregateUser)
admin.site.register(Group)
admin.site.register(Event)
admin.site.register(Activity)
