from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# Only MVP for each model at the moment


class User(AbstractUser):
    avatar = models.ImageField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return self.username


class Group(models.Model):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='user_groups')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups')

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events')
    voting = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    vote_closing_time = models.DateTimeField()

    def __str__(self):
        return self.title


class EventOption(models.Model):
    title = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='options')
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


# class Vote(models.Model):
#     voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
#     # talk to group about on delete CASCADE here ^^
#     event_option = models.ForeignKey(EventOption, on_delete=models.CASCADE, related_name='votes')
#     vote = models.IntegerField(
#         default=0,
#         validators=[MaxValueValidator(1), MinValueValidator(-1)]
#     )
