# Generated by Django 4.1.7 on 2023-03-02 16:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("congregate", "0019_alter_event_vote_closing_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="vote_closing_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 3, 3, 16, 21, 16, 355454, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.CreateModel(
            name="Upload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(blank=True, null=True, upload_to="media/")),
                ("image", models.ImageField(blank=True, null=True, upload_to="media/")),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="uploads",
                        to="congregate.activity",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="uploads",
                        to="congregate.group",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="uploads",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]