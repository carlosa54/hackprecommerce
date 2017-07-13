from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import paypalrestsdk
import json
from django.contrib import messages
from carts.models import Cart
# Create your views here.

class PaymentCheckoutView(TemplateView):

	template_name = 'payments/pay.html'
	def get(self, request, *args, **kwargs):
		template = self.template_name
		if request.GET.get('paymentId'):
			payment = paypalrestsdk.Payment.find(request.GET.get('paymentId'))

			if payment.execute({"payer_id": request.GET.get('PayerID')}):
				context = {
						"done": True
				}
				print("Payment execute successfully")
				return render(request,template,context)
			else:
				print(payment.error)
		cart = Cart.objects.get(id=self.request.session.get("cart_id"))
		print 'GET'
		context = {
			"cart": cart
		}
		template = self.template_name
		return render(request,template,context)

	def post(self, request, *args, **kwargs):
		print 'hello im in PayPal payment'
		cart_id = request.POST.get("cart_id")
		cart = Cart.objects.get(id=cart_id)
		template = self.template_name
		items = {"items": [] }
		paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "ASluobkrXG6eJFzWZrsOGYcGRsX4nCccaB4Cu-5LNQCoNCECtQWMVj651zC5450UPE5dESuUXEOk1xhT",
  "client_secret": "ED5GGT1at1Sa72_ptLqM9FawEic_n58r6zHnQK_V1K1iKlPMiD8y1oFu7L0lmoV8rjF5lshOVOUg6ced" })
		for item in cart.cartitem_set.all():
			items["items"].append(
				{
					"quantity": item.quantity,
					"name": item.item.title,
					"price": str(item.item.price),
					"currency": "USD",
					"description": item.item.description,
				})
		
		payment = paypalrestsdk.Payment({
				"intent": "sale",
				"redirect_urls": 
				{
						"return_url": "http://127.0.0.1:8000/payment",
   						"cancel_url": "http://127.0.0.1:8000"
  					},
  				"payer":
					  {
					    "payment_method": "paypal"
					  },
				"transactions": [
					  {
					    "amount":
					    {
					      "total": str(cart.total + 5) ,
					      "currency": "USD",
					      "details":
					      {
					        "subtotal": str(cart.subtotal),
					        "shipping": '5',
					      }
					    },
					    "item_list": items,
					    "description": "The payment transaction description.",
					    "invoice_number": str(cart.id),
					    "custom": "merchant custom data"
					  }]
			})
		if payment.create():
			for link in payment.links:
				if link.method == "REDIRECT":
					redirect_url = str(link.href)
					print("Redirect for approval: %s" % (redirect_url))
			del request.session["cart_id"]
			return redirect(redirect_url)
  			print("Payment created successfully")
  			messages.success(request, "Thank you for your order.")
		else:
  			print(payment.error)

		context = {
			"test": "dummy"
		}
		return render(request, template, context)
