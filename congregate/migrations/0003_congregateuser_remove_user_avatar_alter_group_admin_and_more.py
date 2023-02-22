# Generated by Django 4.1.7 on 2023-02-22 21:08

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "congregate",
            "0002_event_remove_user_bio_remove_user_birth_date_group_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="CongregateUser",
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
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                ("email", models.EmailField(max_length=254)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="media/"),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="user",
            name="avatar",
        ),
        migrations.AlterField(
            model_name="group",
            name="admin",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="admin_groups",
                to="congregate.congregateuser",
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="members",
            field=models.ManyToManyField(
                related_name="user_groups", to="congregate.congregateuser"
            ),
        ),
    ]