from django.shortcuts import render,redirect
from django.contrib.auth import logout
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html' , {'form':form})

def user_logout(request):
    logout(request)
    return render(request,'users/logout.html')