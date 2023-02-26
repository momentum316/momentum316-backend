from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.

# Only MVP for each model at the moment


class User(AbstractUser):

    def __str__(self):
        return self.username


class CongregateUser(models.Model):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='media/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Group(models.Model):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(CongregateUser, related_name='user_groups')
    admin = models.ForeignKey(CongregateUser, on_delete=models.CASCADE, related_name='admin_groups')

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='events')
    voting = models.BooleanField(default=False)
    date = models.DateTimeField()
    vote_closing_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=24))
    event_voter = models.ManyToManyField(CongregateUser, related_name='voted_events', blank=True)
    decided = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Activity(models.Model):
    title = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='activities')
    creator = models.ForeignKey(CongregateUser, on_delete=models.CASCADE, related_name='activities', null=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class Vote(models.Model):
    voter = models.ForeignKey(CongregateUser, on_delete=models.CASCADE, related_name='votes')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='votes')
    vote = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(1), MinValueValidator(-1)]
    )
