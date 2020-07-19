from django.shortcuts import render

# Create your views here.
def index(request):
    text = "abcdef"
    context = {'text': text}
    return render(request, 'index.html', context)