from celery import shared_task
from django.db.models import Sum
from django.utils import timezone
from .models import Event, Activity
from celery import Celery


@shared_task
def decide_event(event_id):
    event = Event.objects.get(id=event_id)

    if not event.decided and timezone.now() >= event.vote_closing_time:
        event_acts = Activity.objects.filter(event=event).annotate(total_votes=Sum('votes__vote')).order_by('-total_votes')

        winning_activity = event_acts[0]
        winning_activity.is_winner = True
        winning_activity.save()

        event_acts[0].is_winner = True
        event.decided = True
        event.save()
