from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'parent',
                    'create_date_time', 'modify_date_time')


admin.site.register(Category, CategoryAdmin)
