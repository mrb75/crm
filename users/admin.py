from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, NotificationType, Notification, RequestLog


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'writer', 'create_date_time',
                    'modify_date_time', 'is_news')


class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date_time',)


class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'user_agent',
                    'referer', 'url', 'method')


admin.site.register(RequestLog, RequestLogAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(User, UserAdmin)
