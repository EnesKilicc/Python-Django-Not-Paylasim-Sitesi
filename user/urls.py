from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    #path('addcomment/<int:id>', views.addcomment, name = 'addcomment')
    path('update/',views.user_update, name = 'user_update'),
    path('password/',views.change_password, name = 'change_password'),
    path('addnote/',views.add_note, name='add_note'),
    path('notes/',views.notes, name='notes'),
    path('comments/',views.comments, name='comments'),
    path('editnote/<int:id>',views.editnote, name='editnote'),
    path('editcomment/<int:id>',views.editcomment, name='editcomment'),

]