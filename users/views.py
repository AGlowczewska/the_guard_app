from django.shortcuts import render
from django.contrib.auth import login, authenticate

from users.forms import SignUpForm
from django.shortcuts import render, redirect
from the_guard.pyrebase_settings import db, auth

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            auth.sign_in_with_email_and_password(email, raw_password)

            '''try:
                auth.sign_in_with_email_and_password(email, raw_password)
                user2 = authenticate(username=username, password=raw_password)
                login(request, user2)
            except:
                print("CREATING USER")
                auth.create_user_with_email_and_password(email, raw_password)
                user2 = authenticate(username=username, password=raw_password)
                login(request, user2)
'''
            return redirect('../')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
