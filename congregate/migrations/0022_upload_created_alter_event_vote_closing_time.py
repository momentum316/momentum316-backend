# Generated by Django 4.1.7 on 2023-03-05 22:32

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("congregate", "0021_activity_is_winner_alter_event_vote_closing_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="upload",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="event",
            name="vote_closing_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 3, 6, 22, 31, 44, 488133, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
