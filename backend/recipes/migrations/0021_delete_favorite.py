# Generated by Django 4.2.5 on 2023-09-28 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_favorite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
