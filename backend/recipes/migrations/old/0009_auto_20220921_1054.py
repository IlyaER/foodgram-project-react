# Generated by Django 2.2.28 on 2022-09-21 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20220921_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.RecipeIngredients', to='recipes.Ingredients'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(through='recipes.RecipesTags', to='recipes.Tag'),
        ),
    ]
