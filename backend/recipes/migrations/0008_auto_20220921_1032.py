# Generated by Django 2.2.28 on 2022-09-21 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20220921_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
    ]
