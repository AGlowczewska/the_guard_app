from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from the_guard.pyrebase_settings import db


def user_rasps():
    return db.child("sensor").get()


@login_required
def rasp_view(request, rasp_serial):
    rooms = user_rasps()

    context = {'rooms': rooms.val(), 'name': rasp_serial}
    return render(request, 'parts/data_area.html', context)


def index(request):
    context = {}
    if request.user.is_authenticated():
        rooms = user_rasps()
        print(rooms.val())
        context = {'rooms': rooms.val()}
        # stream = db.child("sensors").stream(stream_handler)
        return render(request, 'index.html', context)
    else:
        return render(request, 'registration/login.html', context)


def connect_rasp(request):
    rooms = user_rasps()
    context = {'rooms': rooms.val()}

    if request.method == 'POST':
        serial = request.POST['serial']
        context['serial'] = serial

        # adding to db
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



