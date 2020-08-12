from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from home.forms import SignUpForm
from home.models import Setting, ContactFormMessage, ContactFormu, UserProfile
from note.models import Category, Note, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Category.objects.all()[:4]
    portfoliodata = Note.objects.all()[:8]
    category = Category.objects.all()
    context = {'setting':setting,'page':'home',
               'sliderdata': sliderdata,
               'category':category,
               'portfoliodata':portfoliodata}
    return render(request, 'index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Mesajınız başarı ile gönderilmiştir Teşekkürler')
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    category = Category.objects.all()
    context = {'setting':setting, 'page':'contact','category':category, 'form': form}
    return render(request, 'contact.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting':setting, 'page':'hakkimizda','category':category}
    return render(request, 'hakkimizda.html', context)
def category_notes(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    notes = Note.objects.filter(category_id=id)
    categorydata = Category.objects.get(pk=id)
    context = {'category':category,'notes':notes,'categorydata':categorydata}
    return render(request, 'notes.html', context)

def note_detail(request,id,slug):
    mesaj = "ürün",id,"/",slug
    note = Note.objects.get(pk=id)
    images = Images.objects.filter(note_id=id)
    category = Category.objects.all()
    comments = Comment.objects.filter(note_id=id,status='True')
    context = {'category': category,
               'note': note,
               'images': images,
               'comments': comments,
               }
    return render(request, 'note_detail.html', context)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return HttpResponseRedirect('/')
            else:
                messages.error(request, "LOGIN HATASI")
                return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {'category': category,

               }
    return render(request,'login.html',context)
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id =current_user.id
            data.image = "images/users/icon.png"
            data.save()
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request,'signup.html',context)