from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from the_guard.pyrebase_settings import db
from backend.models import *
from django.db import IntegrityError


@login_required
def rename(request, rasp_serial):
    rooms = user_rasps(request.user.username)
    context = {'rooms': rooms, 'serial': rasp_serial}

    if request.method == 'POST':
        name = request.POST['name']
        my_rasp = Rasps.objects.filter(serial=rasp_serial)[0]
        my_rasp.name = name
        try:
            my_rasp.save()
            rooms = user_rasps(request.user.username)
            context = {'rooms': rooms, 'serial': rasp_serial, 'msg': 'Successfully updated to db'}
        except IntegrityError as err:
            context['msg'] = 'ERROR: Integrity error!'
        except Exception as err:
            context['msg'] = err
        return render(request, 'index.html', context)

    return render(request, 'parts/rename.html', context)


@login_required
def change_armed_status(request, rasp_serial):
    rasp = Rasps.objects.filter(serial=rasp_serial)[0]
    is_armed = rasp.isArmed
    rasp.isArmed = not is_armed
    rasp.save()
    rooms = user_rasps(request.user.username)
    is_armed = rooms[rasp_serial]['isArmed']
    del rooms[rasp_serial]['isArmed']
    context = {'rooms': rooms, 'name': rooms[rasp_serial]['name'], 'serial': rasp_serial,
               'isArmed': is_armed}
    return render(request, 'parts/data_area.html', context)


def user_rasps(username):
    firebase_result = db.child("sensor").get().val()
    my_rasps = Rasps.objects.filter(owner=username).values()
    result = firebase_result.copy()
    for firebase_rasp in firebase_result:
        to_delete = True
        name = ''
        is_armed = True
        for django_rasp in my_rasps:
            if django_rasp['serial'] == firebase_rasp:
                to_delete = False
                name = django_rasp['name']
                is_armed = django_rasp['isArmed']
        if to_delete:
            del(result[firebase_rasp])
            print('Not in result - deleted: ', firebase_rasp)
        else:
            result[firebase_rasp]['name'] = name
            result[firebase_rasp]['isArmed'] = is_armed

    return result


@login_required
def rasp_view(request, rasp_serial):
    rooms = user_rasps(request.user.username)
    is_armed = rooms[rasp_serial]['isArmed']
    # del rooms[rasp_serial]['isArmed']
    context = {'rooms': rooms, 'name': rooms[rasp_serial]['name'], 'serial': rasp_serial,
               'isArmed': is_armed}
    return render(request, 'parts/data_area.html', context)


@login_required
def notifications(request, rasp_serial):
    rasp_notifications = Notification.objects.filter(rasp__serial=rasp_serial).values()
    rooms = user_rasps(request.user.username)
    context = {'rooms': rooms, 'notifications': rasp_notifications}
    return render(request, 'parts/rasp_notifications.html', context)


def index(request):
    context = {}
    if request.user.is_authenticated():
        rooms = user_rasps(request.user.username)
        context = {'rooms': rooms}
        # stream = db.child("sensors").stream(stream_handler)
        return render(request, 'index.html', context)
    else:
        return render(request, 'registration/login.html', context)


@login_required
def connect_rasp(request):
    rooms = user_rasps(request.user.username)
    context = {'rooms': rooms}

    if request.method == 'POST':
        serial = request.POST['serial']
        name = request.POST['name']
        context['serial'] = serial
        username = request.user.username
        my_rasp = Rasps(owner=username, name=name, serial=serial)
        # adding to db
        try:
            my_rasp.save()
            context['msg'] = 'Successfully added to db'
        except IntegrityError as err:
            context['msg'] = 'ERROR: This serial already exists in database!'
        except Exception as err:
            context['msg'] = err
        return render(request, 'parts/add_rasp.html', context)

    return render(request, 'parts/add_rasp.html', context)


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
