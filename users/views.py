from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from . forms import RegisterForm

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('budgets:home'))

def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user =  authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('budgets:home'))
    context = {'form': form}
    return render(request, 'users/register.html', context)