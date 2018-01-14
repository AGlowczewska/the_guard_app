from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from the_guard.pyrebase_settings import db
from django.http import HttpRequest


@login_required
def rasp_view(request, rasp_serial):
    context = {}
    rooms = db.child("sensor").get()

    context = {'rooms': rooms.val(), 'name': rasp_serial}
    return render(request, 'parts/data_area.html', context)


def index(request):
    context = {}
    if request.user.is_authenticated():
        rooms = db.child("sensor").get()
        print(rooms.val())
        context = {'rooms': rooms.val()}
        # stream = db.child("sensors").stream(stream_handler)
        return render(request, 'index.html', context)
    else:
        return render(request, 'registration/login.html', context)


def stream_handler(message):
    # print('event:' + message["event"])  # put
    # print('path: ' + message["path"])  # /-K7yGTTEp7O549EzTYtI
    # print(message["data"])  # {'title': 'Pyrebase', "body": "etc..."}
    path = message['path']
    value = message['data']
    context = {'danger_path': path, 'danger_value': value}
    print(context)
    # request = HttpRequest()
    # return render(request, 'index.html', context)



