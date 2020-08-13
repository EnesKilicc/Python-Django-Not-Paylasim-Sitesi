from django.contrib import admin

from home.models import Setting, ContactFormMessage, UserProfile, FAQ


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','status']
    list_filter = ['status']
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','university','image_tag']
    list_filter = ['university']
class FaqAdmin(admin.ModelAdmin):
    list_display = ['ordernumber', 'question', 'answer', 'status']
    list_filter = ['status']
admin.site.register(Setting)
admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(FAQ,FaqAdmin)