# Generated by Django 2.2.28 on 2022-09-19 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribe',
            name='subscribed_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed', to=settings.AUTH_USER_MODEL, verbose_name='На кого подписан'),
        ),
        migrations.AddField(
            model_name='subscribe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddField(
            model_name='recipestags',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='recipestags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Tag'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(related_name='recipe', through='recipes.Ingredients', to='recipes.Components'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(through='recipes.RecipesTags', to='recipes.Tag'),
        ),
        migrations.AddField(
            model_name='ingredients',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Components'),
        ),
        migrations.AddField(
            model_name='ingredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('user', 'subscribed_to'), name='unique subscribers'),
        ),
    ]
