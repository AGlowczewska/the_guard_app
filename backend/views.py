import json

import firebase_admin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials, auth
from rest_framework.decorators import api_view

from pyfcm import FCMNotification
from backend.models import Rasps
from backend.models import FCMTokens

initialized = False

#kurwa siedzialem nad tym 2h a okazalo sie ze jest blad w fcmnotification  i to nie jest api_key tylko SERVER_KEY !!! JPRDL
push_service = FCMNotification(api_key="AAAARdiLvpk:APA91bGYmQFiCd-ltjrgp-IVbG30kYH0z7i9hShZsA-ZkwwoRS7RgjOgNRD0G6rVyioq6m_0KBg9FSWCNjLdqG8D2DGiMNjkJkJRaTmhwJc_OPS1frV1p-XauTea7fx49N7fdscYPIGD")


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
    device, created = Rasps.objects.get_or_create(serial=serial, defaults={'owner': owner, 'name' : name})
    
    #camera = Rasps(serial=serial, owner=owner, name=name)
    #camera.save()
    print("Added Camera to DB: serial: {} owner: {} name: {}".format(serial, owner, name))
    return


def filter_devices(owner):
    print("Get Cameras by Owner: {}".format(owner))
    data = Rasps.objects.filter(owner=owner)
    return data


def change_device_ownership(owner, serial_nr):
    device = Rasps.objects.get(serial=serial_nr)
    device.owner = owner
    device.save()
    print("Updated object: {0}".format(device))
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
        owner = body['owner']
        authorize_request(body['token'])
        device, created = Rasps.objects.get_or_create(serial=serial, defaults={'owner': owner, 'name' : 'Guard', 'isArmed' : True})
        if created:
            return HttpResponse(content_type = "application/json",status_code = 200)
    else:
        return HttpResponse(content_type = "application/json",status_code = 400)


# PATH: /backend/v1/devices/get
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
    else:
        return HttpResponse(content_type = "application/json",status_code = 400)


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
        return HttpResponse(info, content_type="application/json")       

# PATH: /backend/v1/notification
@api_view(['POST'])
@csrf_exempt
def notification(request):
    print("notification")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        info = ""
        serial = ""
        sensorTypes = []
        for item in body:
            sensorType = item["sensorType"]
            value = item["value"]
            serial = item["serial"]
            sensorTypes.append(sensorType)

        ids = []
        messageBody = ""
        messageTitle = ""

        rasp = Rasps.objects.filter(serial=serial)[0]
        for sensorType in sensorTypes:
            if(sensorType=="COSensor"):
                info += "High Value of CO\n"
            if(sensorType=="LPGSensor"):
                info += "High Value of LPG\n"
            if(sensorType=="FlameSensor"):
                info += "Fire detected!\n"
            if(sensorType=="TempSensor"):
                info += "High Value of Temp"

        messageBody = "Alert from %s" % (rasp.name)
        messageTitle = info
        for fcm in FCMTokens.objects.filter(email=rasp.owner):
            ids.append(fcm.fcmToken)
        
   
        result = push_service.notify_multiple_devices(registration_ids=ids, message_title=messageTitle, message_body=messageBody)
        info = [{'info': 'success'}]
        json_data = json.dumps(info)
        json_data = str(json_data)
        return HttpResponse(json_data, content_type="application/json")

# PATH: /backend/v1/fcmTokenUpdate
@api_view(['POST'])
@csrf_exempt
def fcmTokenUpdate(request):
    print("tokenUpdate")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email']
        token = body['fcmToken']
        deviceId = body['deviceId']

        obj, created = FCMTokens.objects.update_or_create(deviceId=deviceId, defaults={'email': email, 'fcmToken': token})

        info = [{'info': 'success'}]
        json_data = json.dumps(info)
        json_data = str(json_data)
        return HttpResponse(json_data, content_type="application/json")

# PATH: /backend/v1/devices/changeRaspName
@api_view(['POST'])
@csrf_exempt
def changeRaspName(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        serial = body['serial']
        name = body['name']
        authorize_request(body['token'])
        obj, created = Rasps.objects.update_or_create(serial=serial, defaults={'name': name})

        info = [{'info': 'success'}]
        json_data = json.dumps(info)
        json_data = str(json_data)
        return HttpResponse(json_data, content_type="application/json")

# PATH: /backend/v1/devices/changeIsArmed
@api_view(['POST'])
@csrf_exempt
def changeIsArmed(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        serial = body['serial']
        armed = body['armed']
        authorize_request(body['token'])
        obj, created = Rasps.objects.update_or_create(serial=serial, defaults={'isArmed': armed})

        info = [{'info': 'success'}]
        json_data = json.dumps(info)
        json_data = str(json_data)
        return HttpResponse(json_data, content_type="application/json")
