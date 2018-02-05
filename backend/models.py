from django.db import models



class Rasps(models.Model):
    owner = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    serial = models.CharField(max_length=250, unique=True)
    isArmed = models.BooleanField(default = True)

class FCMTokens(models.Model):
    email = models.CharField(max_length=100)
    fcmToken = models.CharField(max_length=300)
    deviceId = models.CharField(max_length=250, unique=True)


class Notification(models.Model):
    notificationType = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add = True)
    message = models.CharField(max_length=250)
    rasp = models.ForeignKey(Rasps, on_delete=models.CASCADE)
    videoURL = models.CharField(max_length=100, default = "")
