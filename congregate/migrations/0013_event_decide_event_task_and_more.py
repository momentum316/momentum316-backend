# Generated by Django 4.1.7 on 2023-02-26 19:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("congregate", "0012_rename_voter_event_event_voter_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="decide_event_task",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="vote_closing_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 2, 27, 19, 18, 6, 491586, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]