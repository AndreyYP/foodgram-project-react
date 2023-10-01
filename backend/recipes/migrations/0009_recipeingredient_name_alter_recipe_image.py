# Generated by Django 4.2.5 on 2023-10-01 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_alter_recipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes_images/'),
        ),
    ]
