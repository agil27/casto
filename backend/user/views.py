from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from .models import User
import re


# Create your views here.
def logon(request):
    if request.method != 'POST':
        return HttpResponse(status=400)
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()
    if username == '' or password == '' or not valid_password(password):
        return JsonResponse({'error': 'invalid parameter'})
    user = User.objects.create(username=username, password=make_password(password))
    user.save()
    return HttpResponse(status=200)


def login(request):
    if request.method != 'POST':
        return HttpResponse(status=400)
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()
    if username == '' or password == '':
        return JsonResponse({'error': 'invalid parameter'})
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'fail to login'})
    django_login(request, user)
    return HttpResponse(status=200)


def logout(request):
    django_logout(request)
    return HttpResponse(status=200)


def valid_password(password):
    reg = r'^[A-Za-z0-9_]{6,18}$'
    if re.match(reg, password):
        has_number = False
        has_letter = False
        num_reg = '[0-9]'
        letter_reg = '[A-Za-z]'
        for c in password:
            if re.match(num_reg, c):
                has_number = True
            if re.match(letter_reg, c):
                has_letter = True
        return has_number and has_letter
    return False
