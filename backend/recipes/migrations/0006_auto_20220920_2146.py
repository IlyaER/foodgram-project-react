# Generated by Django 2.2.28 on 2022-09-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20220920_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(default='default text', max_length=1200),
            preserve_default=False,
        ),
    ]
