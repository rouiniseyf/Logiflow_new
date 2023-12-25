from django.shortcuts import render , redirect
from django.http import HttpResponse
from ..models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def get_full_name(self):
    return  self.last_name + " " + self.first_name

User.add_to_class("__str__", get_full_name)

def register(request): 
    form = CreateUserForm()
    if request.method == "POST" :
        getten_form = CreateUserForm(request.POST)
        if getten_form.is_valid: 
            getten_form.save()

    return render(request,'TonersManagement/pages/register.html', {'form': form})


def loginpage(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,"Veuillez saisir un nom d'utilisateur et un mot de passe valides", extra_tags="danger")
            return redirect('/login')

    return render(request,'app/pages/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')
