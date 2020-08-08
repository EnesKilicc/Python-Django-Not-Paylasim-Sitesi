from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormMessage, ContactFormu
from note.models import Category

def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Category.objects.all()[:4]
    category = Category.objects.all()
    context = {'setting':setting,'page':'home',
               'sliderdata': sliderdata,
               'category':category}
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
    context = {'setting':setting, 'page':'contact', 'form': form}
    return render(request, 'contact.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting':setting, 'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)