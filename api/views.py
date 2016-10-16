from django.shortcuts import render
from django.views.generic import TemplateView
import requests

# Create your views here.
def token_login():
	payload = {"commUsername":"carlosa", "commPassword":"1234ab12"}
	response = requests.get("http://athmapi.westus.cloudapp.azure.com/athm/requestSession", params=payload)
	return response.json()["token"]

class ATHMovilCheckoutView(TemplateView):
	template_name = 'api/athmovil.html'

	def get(self, request, *args, **kwargs):
		token = token_login()

		context = {
			"token": token
		}


		template = self.template_name
		return render(request,template,context)


