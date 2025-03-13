# Generated by Django 5.1.7 on 2025-03-13 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_userprofile_diet_preference_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='hearted_recipes',
            field=models.ManyToManyField(blank=True, related_name='hearted_by_users', to='profiles.savedrecipe'),
        ),
    ]
