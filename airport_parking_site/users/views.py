from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form .save()
            login = form.cleaned_data.get('username')
            messages.success(request, 'Utworzono konto dla {}'.format(login))
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_redirect(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('parking_app-home-admin')
    else:
        return redirect('parking_app-home-client')
