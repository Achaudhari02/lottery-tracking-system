from django.shortcuts import render, redirect
from django.http import request
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def base(request):
    return render(request, 'inventory/home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None: 
            login(request,user)
            return redirect('base')
        else: 
            messages.error(request, "The user does not exist") 
            

            
    return render(request, 'accounts/login.html')

@login_required
def logout_user(request):
    if request.method == 'GET':
        logout(request)
    return redirect('login')