from django.contrib import admin

from home.models import Setting, ContactFormMessage, UserProfile


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','status']
    list_filter = ['status']
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','university','image_tag']
    list_filter = ['university']

admin.site.register(Setting)
admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(UserProfile,UserProfileAdmin)