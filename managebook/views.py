# from django.http import HttpResponse
from django.shortcuts import render

# def  hello(request):
# return HttpResponse('Hello World')


def hello(request):
    response = {'user': 'Gleb', 'digit': 2020}
    return render(request, 'index.html', response)
