from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from carts.views import Cart
import requests
from .models import Payment
from .mixins import TokenMixin

# Create your views here.

class ATHMovilCheckoutView(TokenMixin, TemplateView):
	template_name = 'api/athmovil.html'

	def get(self, request, *args, **kwargs):
		template = self.template_name

		context = {
			"cart_id": request.GET.get("cart_id"),
		}
		return render(request,template,context)

	def post(self, request, *args, **kwargs):
		token = self.token_login()
		response = ''
		template = self.template_name

		if request.POST.get('phone') and request.POST.get("cart_id") :
			print request.POST.get('phone')
			cart_id = request.POST.get("cart_id")
			
			cart = Cart.objects.get(id=cart_id)
			parameters = {"token": token, "phone": request.POST.get('phone'), "amount":cart.total}
			response = requests.get("http://athmapi.westus.cloudapp.azure.com/athm/requestPayment", params=parameters)

			if response.json()["responseStatus"] == "SUCCESS":
				cart.is_complete()
				del request.session["cart_id"]
				response = response.json()
				payment, created = Payment.objects.get_or_create(cart=cart)
				if created:
					payment.amount = cart.total
					payment.referenceNumber = response["referenceNumber"]
					payment.phone = response["phone"]
					payment.save()

				context = {
					"success": True
				}
				return render(request, template, context)

			context = {
				"success": False
			}
		return render(request, template, context)

class PaymentList(ListView):
	model = Payment

