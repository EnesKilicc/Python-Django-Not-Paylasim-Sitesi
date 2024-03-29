from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from note.models import Category, Note, Images, Comment


# Register your models here.
class NoteImageInline(admin.TabularInline):
    model = Images
    extra = 5
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['title']
    list_display = ['title', 'status', 'keywords','image_tag']
    readonly_fields = ('image_tag',)
class NoteAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display = ['title','category', 'status','image_tag' , 'keywords','user','status']
    readonly_fields = ('image_tag',)
    inlines = [NoteImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'note', 'image_tag']
    readonly_fields = ('image_tag',)


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_notes_count', 'related_notes_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Note,
                'category',
                'notes_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Note,
                 'category',
                 'notes_count',
                 cumulative=False)
        return qs

    def related_notes_count(self, instance):
        return instance.notes_count
    related_notes_count.short_description = 'Related notes (for this specific category)'

    def related_notes_cumulative_count(self, instance):
        return instance.notes_cumulative_count
    related_notes_cumulative_count.short_description = 'Related notes (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment','note','user','status']
    list_filter = ['status']

admin.site.register(Category, CategoryAdmin2)
admin.site.register(Note, NoteAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Comment,CommentAdmin)
