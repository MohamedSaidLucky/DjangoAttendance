from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_custom_view(request):
    return HttpResponse('Admin Custom View')