from django.contrib import admin

from recipes.models import *


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'fav_count')
    #search_fields = ('text',)
    list_filter = ('author', 'name', 'tags')
    #list_editable = ('group',)
    empty_value_display = '-пусто-'
    readonly_fields = ('fav_count',)
    fields = ('author', 'name', 'image', 'text', 'cooking_time', 'fav_count')

    def fav_count(self, obj):
        return obj.favorite.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')#'author', 'fav_count')
    search_fields = ('name', )

admin.site.register(Tag)
#admin.site.register(Ingredient)
#admin.site.register(Recipe)

