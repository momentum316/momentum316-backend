# Generated by Django 4.1.7 on 2023-02-28 16:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("congregate", "0015_user_avatar_alter_event_vote_closing_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="creator",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="activities",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="event_voter",
            field=models.ManyToManyField(
                blank=True, related_name="voted_events", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="vote_closing_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 3, 1, 16, 53, 54, 794445, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="admin",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="admin_groups",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="members",
            field=models.ManyToManyField(
                related_name="user_groups", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="voter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
