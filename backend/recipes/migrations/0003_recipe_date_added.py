# Generated by Django 2.2.28 on 2022-09-30 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220930_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
    ]