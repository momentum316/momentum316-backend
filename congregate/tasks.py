from celery import shared_task
from django.utils import timezone
from .models import Event
from celery import Celery


@shared_task
def decide_event(event_id):
    event = Event.objects.get(id=event_id)

    if not event.decided and timezone.now() >= event.vote_closing_time:
        event.decided = True
        event.save()
