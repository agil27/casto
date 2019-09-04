from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from .models import User
import re


# Create your views here.
def index(request):
    return render(request, 'user/index.html', {})

def signup(request):
    print(request)
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        print(username, password)
        if username == '' or password == '' or not valid_password(password): 
            return JsonResponse({'error': 'invalid parameter'})
        user = User.objects.create(username=username, password=make_password(password))
        user.save()
        return JsonResponse({'username': username, 'status': True})
        # return render(request, 'user/login.html', {})
    elif request.method == 'GET':
        return render(request, 'user/signup.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username == '' or password == '':
            return JsonResponse({'error': 'invalid parameter'})
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'fail to login'})
        django_login(request, user)
        return HttpResponse(status=200)
    elif request.method == 'GET':
        return render(request, 'user/login.html', {})

def dashboard(request):
    if request.method == 'GET':
        return render(request, 'user/dashboard.html')
        
def logout(request):
    django_logout(request)
    return HttpResponse(status=200)


def please_login(_):
    return JsonResponse({'error': 'please login'})


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
