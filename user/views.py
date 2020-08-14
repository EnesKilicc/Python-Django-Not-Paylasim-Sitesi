from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from home.models import Setting, UserProfile
from note.models import Category, Note, Comment
from user.form import UserUpdateForm, ProfileUpdateForm, InsertNoteForm, EditCommentForm


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'PROFİLİNİZ GUNCELLENDİ')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category':category,
            'user_form':user_form,
            'profile_form':profile_form,
        }
        return render(request,'user_update.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"Sifreniz Basarıyla Güncellendi")
            return redirect('change_password')
        else:
            messages.error(request,"Please Correct the error below.<br>" + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',{
            'form': form,
            'category':category
        })

@login_required(login_url='/login')
def add_note(request):
    if request.method == 'POST':
        form = InsertNoteForm(request.POST,request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Note()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.okul = form.cleaned_data['okul']
            data.egitmen = form.cleaned_data['egitmen']
            data.ders = form.cleaned_data['ders']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.category = form.cleaned_data['category']
            data.status = 'False'
            data.save()
            messages.success(request, "Notunuz Admin Onayından Sonra Paylaşılacak")
            return HttpResponseRedirect('/user')
        else:
            messages.success(request,"bir hata olustu")
            return HttpResponseRedirect('/')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = InsertNoteForm()
        context = {'category':category,
                   'setting':setting,
                   'form': form,
                   }
        return render(request,'user_add_note.html',context)

@login_required(login_url='/login')
def notes(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    notes = Note.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'setting': setting,
               'notes': notes,
               }
    return render(request,'user_notes.html',context)
@login_required(login_url='/login')
def comments(request):

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'setting': setting,
               'comments': comments,
               }
    return render(request, 'user_comments.html', context)

def editnote(request,id):
    note = Note.objects.get(id=id)
    if request.method == 'POST':
        form = InsertNoteForm(request.POST,request.FILES,instance=note)
        note.status = 'Update'
        if form.is_valid():
            form.save()
            messages.success(request,"Güncelleme basarıyla yapıldı")
            return HttpResponseRedirect('/user/notes')
        else:
            messages.success(request,"Güncelleme Hatası" + str(form.errors))
            return HttpResponseRedirect('/user/editnote/'+str(id))
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = InsertNoteForm(instance=note)
        context = {'category':category,
                   'setting':setting,
                   'form':form}
        return render(request, 'user_add_note.html', context)

def editcomment(request,id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        form = EditCommentForm(request.POST,request.FILES,instance=comment)
        comment.status = 'Update'
        if form.is_valid():
            form.save()
            messages.success(request,"Güncelleme basarıyla yapıldı")
            return HttpResponseRedirect('/user/comments')
        else:
            messages.success(request,"Güncelleme Hatası" + str(form.errors))
            return HttpResponseRedirect('/user/editcomment/'+str(id))
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        form = EditCommentForm(instance=comment)
        context = {'category':category,
                   'setting':setting,
                   'form':form}
        return render(request, 'user_edit_comment.html', context)




def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'setting':setting,
               'category':category,
               'profile':profile,
               }

    return render(request,'user_profile.html',context)