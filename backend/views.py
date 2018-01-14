import json

import firebase_admin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials, auth
from rest_framework.decorators import api_view

from backend.models import Rasps

initialized = False

def initialize_firebase_admin_sdk():
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)


def authorize_request(token):
    global initialized
    if token == "debug":
        print("Debug token authorized")
        return
    if initialized == False:
        initialize_firebase_admin_sdk()
        initialized = True

    decoded_token = auth.verify_id_token(token)
    print("Verified token: {}".format(decoded_token))


def add_device_to_database(serial, owner, name):
    camera = Rasps(serial=serial, owner=owner, name=name)
    camera.save()
    print("Added Camera to DB: serial: {} owner: {} name: {}".format(serial, owner, name))
    return


def filter_devices(owner):
    print("Get Cameras by Owner: {}".format(owner))
    data = Rasps.objects.filter(owner=owner)
    return data


def change_device_ownership(owner, serial_nr):
    print("Getting rasps")
    rasp = Rasps.objects.get(serial=serial_nr)
    rasp.owner = owner
    rasp.save()

    print("Updated object: {0}".format(rasp))
    return


# PATH: /backend/v1/camera_address/
@api_view(['POST'])
@csrf_exempt
def get_test_address(request):
    if request.method == 'POST':
        data = {"id": "http://52.236.165.15:80/hls/test.m3u8"}
        dump = json.dumps(data)
        return HttpResponse(dump, content_type="application/json")


# PATH /backend/v1/devices/add/
@api_view(['POST'])
@csrf_exempt
def register_rasp(request):
    context = {}
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        serial = body['serial']

        authorize_request(body['token'])

        add_device_to_database(serial, "", "Camera")
        context = {'msg': 'Successfully added to the database'}
        return render(request, 'rasp_edit.html', context)
    return render(request, 'rasp_edit.html', context)


# PATH: /backend/v1/devices
@api_view(['POST'])
@csrf_exempt
def get_devices_for_owner(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        owner = body['owner']
        authorize_request(body['token'])

        camera_list = filter_devices(owner)

        device_list = []
        for camera in camera_list:
            device = {'serial': camera.serial, 'name': camera.name}
            device_list.append(device)

        json_data = json.dumps(device_list)
        json_data = str(json_data)
        return HttpResponse(json_data, content_type="application/json")


# PATH: /backend/v1/devices/assign
@api_view(['POST'])
@csrf_exempt
def assign_device_to_owner(request):
    context = {}
    print("assiginng")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        serial = body['serial']
        owner = body['owner']
        authorize_request(body['token'])
        change_device_ownership(owner, serial)
        context = {'msg': 'Ownership successfully changed'}
        info = {'info': 'success'}
        #json_data = json.dumps(info)
        #json_data = str(json_data)
        return HttpResponse(info, content_type="application/json")       
        #return render(request, 'rasp_edit.html', context)


# PATH: /backend/v1/notification
@api_view(['POST'])
@csrf_exempt
def notification(request):
    print("notification")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        for item in body:
            sensorType = item['sensorType']
            value = item['value']
            serial = item['serial']
            print(serial) 
            print(sensorType)

        info = [{'info': 'success'}]
        json_data = json.dumps(info)
        json_data = str(json_data)
        return HttpResponse(json_data, content_type="application/json")
