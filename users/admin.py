from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, NotificationType, Notification, RequestLog, Country, Province, City


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_code')


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province_id')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'writer', 'create_date_time',
                    'modify_date_time', 'is_news')


class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date_time',)


class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'user_agent',
                    'referer', 'url', 'method')


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'mobile', 'birth_date', 'company_name', 'admin')
        }),
    )


admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(RequestLog, RequestLogAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(User, CustomUserAdmin)
