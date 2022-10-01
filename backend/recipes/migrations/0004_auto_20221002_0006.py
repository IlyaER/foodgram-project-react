# Generated by Django 2.2.28 on 2022-10-01 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_date_added'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-date_added',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Метка', 'verbose_name_plural': 'Метки'},
        ),
    ]
