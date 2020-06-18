from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, KlientForm
from django.db import transaction

# Create your views here.


@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        client_form = KlientForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            user.save()
            profile = client_form.save(commit=False)
            profile.user = user
            profile.save()

            login = user_form.cleaned_data.get('username')
            messages.success(request, 'Utworzono konto dla {}'.format(login))
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        client_form = KlientForm()

    context = {
        'user_form': user_form,
        'client_form': client_form
    }
    return render(request, 'users/register.html', context)
