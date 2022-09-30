from django.contrib import admin
from users.models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', )
    list_filter = ('email', 'username', )
