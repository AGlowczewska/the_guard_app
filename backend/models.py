from django.db import models
    #return render(request, 'rasp_edit.html', context)


class Rasps(models.Model):
    owner = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    serial = models.CharField(max_length=250, unique=True)
    isArmed = models.BooleanField(default = True)

class FCMTokens(models.Model):
    email = models.CharField(max_length=100)
    fcmToken = models.CharField(max_length=300)
    deviceId = models.CharField(max_length=250, unique=True)

