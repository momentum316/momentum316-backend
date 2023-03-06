from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    avatarURL = models.URLField(max_length=1000, null=True)
    # avatar = models.ImageField(upload_to='media/', blank=True, null=True)

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
    date = models.DateTimeField()
    vote_closing_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=24))
    event_voter = models.ManyToManyField(User, related_name='voted_events', blank=True)
    decided = models.BooleanField(default=False)
    decide_event_task = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            from .tasks import decide_event
            decide_event_task = decide_event.apply_async(args=[self.id], eta=self.vote_closing_time).id
            self.decide_event_task = decide_event_task
            self.save()
        else:
            existing_event = Event.objects.get(pk=self.pk)
            if existing_event.vote_closing_time != self.vote_closing_time:
                from .tasks import decide_event
                if self.decide_event_task is not None:
                    decide_event.AsyncResult(self.decide_event_task).revoke()
                if not self.decided:
                    decide_event_task = decide_event.apply_async(args=[self.id], eta=self.vote_closing_time).id
                    self.decide_event_task = decide_event_task
                else:
                    self.decide_event_task = None

            super().save(*args, **kwargs)


class Activity(models.Model):
    title = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='activities')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    description = models.TextField()
    location = models.TextField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_winner = models.BooleanField(default=False)
    attendees = models.ManyToManyField(User, related_name='attending_activities', blank=True)

    def __str__(self):
        return self.title


class PendingActivity(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pending_activities')
    description = models.TextField()
    location = models.TextField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    image = models.URLField(null=True)

    def __str__(self):
        return self.title


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='votes')
    vote = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(1), MinValueValidator(-1)]
    )


class Upload(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='uploads', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='uploads', null=True, blank=True)
    file = models.FileField(upload_to='media/', blank=True, null=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
