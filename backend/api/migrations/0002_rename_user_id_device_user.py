# Generated by Django 5.0.6 on 2024-05-11 21:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="device",
            old_name="user_id",
            new_name="user",
        ),
    ]
