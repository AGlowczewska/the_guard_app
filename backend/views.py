from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from backend.models import Rasps


def delete_rasp_from_db(serial_nr):
    try:
        rasp = Rasps.objects.get(serial=serial_nr)
        rasp.delete()
        print("Object {0} has been deleted".format(rasp))
        return True
    except Rasps.DoesNotExist:
        print("User does not exist")
        return False


def add_cam_to_db(serial, owner, name):
    camera = Rasps(serial=serial, owner=owner, name=name)
    camera.save()
    print("Added Camera to DB: serial: {} owner: {} name: {}".format(serial, owner, name))
    return


def get_camera_owner(owner):
    print("Get Cameras by Owner: {}".format(owner))
    data = Rasps.objects.filter(owner=owner)
    return data


def set_camera_owner(owner, serial_nr):
    rasp = Rasps.objects.get(serial=serial_nr)
    rasp.owner = owner
    rasp.save()

    print("Updated object: {0}".format(rasp))
    return


# PATH: /backend/v1/camera_address/
@api_view(['GET'])
def get_test_address(request):
    if request.method == 'GET':
        data = {"id": "http://52.236.165.15:80/hls/test.m3u8"}
        dump = json.dumps(data)
        return HttpResponse(dump, content_type="application/json")


@login_required
def register_rasp(request):
    context = {}
    if request.method == 'POST':
        serial = request.POST['serial']
        add_cam_to_db(serial, "", "Camera")
        context = {'msg': 'Successfully added to the database'}
        return render(request, 'rasp_edit.html', context)
    return render(request, 'rasp_edit.html', context)


# PATH: /backend/v1/get_cameras/<owner>/
@api_view(['GET'])
def get_rasps(request):
    if request.method == 'GET':
        # read owner from request
        owner = request.GET['owner']
        # receive list of his rasps
        cameras_list = get_camera_owner(owner)
        rasp_ids = []
        for camera in cameras_list:
            temp = {'id': camera.id, 'name': camera.name}
            rasp_ids.append(temp)

        json_data = json.dumps(rasp_ids)
        json_data = str(json_data)
        return HttpResponse(json_data, content_type="application/json")


# PATH: /backend/v1/connect/
@api_view(['POST'])
def connect_rasp_with_user(request):
    context = {}
    if request.method == 'POST':
        # receive from json user and rasp serial
        serial = request.POST['serial']
        owner = request.POST['owner']
        set_camera_owner(owner, serial)
        context = {'msg': 'Successfully updated to the database'}
        return render(request, 'rasp_edit.html', context)
    return render(request, 'rasp_edit.html', context)


# TO DO BELOW





@api_view(['POST'])
def sensors_update(request, format=json):
    if request.method == 'POST':
        b_json = request.body.decode('utf-8')
        data_json = json.loads(b_json)
        owner = data_json['email']
        raspberry = data_json['serial']
        # get devices connected with raspi
        # send to firebase POST request with data: devicesIDs and sensor data
        # send back 200
        return


# PATH: /v1/delete
@api_view(['POST'])
def delete_rasp(request):
    if request.method == 'POST':
        return
