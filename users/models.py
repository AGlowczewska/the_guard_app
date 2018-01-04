from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def show_name(self):
        return "This is " + self.name

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password
