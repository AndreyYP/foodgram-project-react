# Generated by Django 4.2.5 on 2023-09-27 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_user_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favorites',
        ),
    ]
