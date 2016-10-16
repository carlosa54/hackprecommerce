import requests
class TokenMixin(object):
	def token_login(self):
		payload = {"commUsername":"carlosa", "commPassword":"1234ab12"}
		response = requests.get("http://athmapi.westus.cloudapp.azure.com/athm/requestSession", params=payload)
		return response.json()["token"]