from django.shortcuts import render
from the_guard.pyrebase_settings import db


def index(request):
    context = {}
    return render(request, 'index.html', context)


def get_users(request):
    users = db.child("users").get()
    return render(request, 'users.html', {'users': users.val()})
