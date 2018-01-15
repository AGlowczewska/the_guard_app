from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from the_guard.pyrebase_settings import auth
import json


# TESTED AND IMPLEMENTED 8.01.2018 #
def logout_user(request):
    logout(request)
    context = {'msg': 'You have been successfull logged out'}
    return render(request, 'registration/login.html', context)


# TESTED AND IMPLEMENTED 8.01.2018 #
def login_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']

        try:
            auth.sign_in_with_email_and_password(username, raw_password)
            try:
                # del_user(request, username)
                user = User.objects.get(username=username)
                user.set_password(raw_password)
                user = authenticate(username=username, password=raw_password)
                login(request, user)
            except User.DoesNotExist:
                user = add_user(username, username, raw_password)
                login(request, user)

            return redirect('../')
        except Exception as err:
            try:
                json_data = json.loads(err.args[1])
                serv_message = 'The server returned error: {0}: {1}'.format(json_data['error']['code'],
                                                                            json_data['error']['message'])
                # print(serv_message)
                context = {'msg': serv_message}
            except:
                context = {'msg': 'Internal error - please check your internet connection'}
    return render(request, 'registration/login.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password']

        try:
            auth.create_user_with_email_and_password(username, raw_password)
            try:
                user = User.objects.get(username=username)
                user.set_password(raw_password)
            except User.DoesNotExist:
                user = add_user(username, username, raw_password)
            context = {'msg': 'User created successfully! Please log in.'}
            return render(request, 'registration/login.html', context)

        except Exception as err:
            try:
                json_data = json.loads(err.args[1])
                if json_data['error']['message'] == 'EMAIL_EXISTS':
                    context = {'msg': 'User already exists! Please log in.'}
                    return render(request, 'registration/login.html', context)
                elif json_data['error']['message'] == 'INVALID_EMAIL':
                    context = {'msg': 'Please provide valid email address.'}
                else:
                    serv_message = 'The server returned error: {0}: {1}'.format(json_data['error']['code'],
                                                                                json_data['error']['message'])
                    context = {'msg': serv_message}
            except:
                context = {'msg': 'Internal error - please check internet connection'}

    return render(request, 'registration/signup.html', context)


def del_user(request, username):
    try:
        u = User.objects.get(username=username)
        u.delete()
        messages.sucess(request, "The user is deleted")
        return True

    except User.DoesNotExist:
        messages.error(request, "User does not exist")
        return False

    except Exception as e:
        return False


def add_user(username, email, password):
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password)
    return user
