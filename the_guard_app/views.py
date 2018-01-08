from django.shortcuts import render
from the_guard.pyrebase_settings import db


def index(request):
    context = {}
    if request.user.is_authenticated():
        return render(request, 'index.html', context)
    else:
        return render(request, 'registration/login.html', context)


def get_users(request):
    users = db.child("users").get()
    return render(request, 'users.html', {'users': users.val()})
