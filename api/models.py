from __future__ import unicode_literals
from django.db import models
from .mixins import TokenMixin
import requests
from django.db.models.signals import pre_save
from carts.models import Cart

# Create your models here.
class Payment(models.Model):
	referenceNumber = models.CharField(max_length=120)
	phone = models.CharField(max_length=120)
	amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	status = models.CharField(max_length=120)
	cart = models.OneToOneField(Cart, null=True)

def check_status_receiver(sender, instance, *args, **kwargs):
	payload = {"commUsername":"carlosa", "commPassword":"1234ab12"}
	response = requests.get("http://athmapi.westus.cloudapp.azure.com/athm/requestSession", params=payload)
	token = response.json()["token"]
	parameters = {"token":token, "referenceNumber": instance.referenceNumber }
	response = requests.get("http://athmapi.westus.cloudapp.azure.com/athm/verifyPaymentStatus", params=parameters)

	instance.status = response.json()["status"]
	



pre_save.connect(check_status_receiver, sender=Payment)
