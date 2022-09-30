from django.contrib import admin

from recipes.models import *


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    #search_fields = ('text',)
    list_filter = ('author', 'name', 'tags')
    #list_editable = ('group',)
    empty_value_display = '-пусто-'
    #fields = ('author', 'name', )

    def fav_count(self, obj):
        return obj.favorite.count()


admin.site.register(Tag)
admin.site.register(Ingredient)
#admin.site.register(Recipe)

