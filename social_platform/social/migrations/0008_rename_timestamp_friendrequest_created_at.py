# Generated by Django 5.2.2 on 2025-06-19 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_friendrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]
