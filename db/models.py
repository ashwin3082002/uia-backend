from django.db import models

# Create your models here.
class CitizenDetail(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120, primary_key=True)
    phone = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)

    def __str__(self):
        return self.email

class ManagerDetail(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120, primary_key=True)
    phone = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    section = models.CharField(max_length=120)
    def __str__(self):
        return self.email


class WorkerDetail(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120, primary_key=True)
    phone = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    manager = models.ForeignKey(ManagerDetail,on_delete=models.CASCADE)
    def __str__(self):
        return self.email
 
