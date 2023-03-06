# Generated by Django 4.1.7 on 2023-03-06 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("congregate", "0025_remove_activity_attendees_event_attendees_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="event",
            name="location",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="group",
            name="avatar",
            field=models.URLField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="vote_closing_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 3, 7, 20, 18, 16, 503229, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]