from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, 'homepage/index.html')

def dashboard(request):
    return HttpResponse("hola")