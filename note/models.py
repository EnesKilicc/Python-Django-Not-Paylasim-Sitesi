from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (('True', 'Evet'),
              ('False', 'Hayır'),
              )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{self.image.url}" height="50"/>')
        else:
            return ""
    image_tag.short_description = 'Image'

class Note(models.Model):
    STATUS = (('True', 'Evet'),
              ('False', 'Hayır'),
              ('Update','Update'),
              )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    okul = models.CharField(max_length=100)
    ders = models.CharField(max_length=100)
    egitmen = models.CharField(max_length=50)
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    category = models.ForeignKey('Category', null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{self.image.url}" height="50"/>')
        else:
            return ""
    image_tag.short_description = 'Image'

class Images(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    image = models.ImageField(blank=True, upload_to='images/')
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="50"/>')
        else:
            return ""
    image_tag.short_description = 'Image'


class Comment(models.Model):
    STATUS = (('New', 'Yeni'),
              ('True', 'Evet'),
              ('False', 'Hayır'),
              ('Update','Update'),
              )
    note = models.ForeignKey(Note,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment']