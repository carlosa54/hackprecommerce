from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import View
from carts.models import Cart, CartItem
from products.models import Product
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.core.urlresolvers import reverse

# Create your views here.
class CartView(SingleObjectMixin, View):
	model = Cart
	template_name = "carts/view.html"

	def get_object(self, *args, **kwargs):
		self.request.session.set_expiry(0)
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			cart = Cart()
			cart.subtotal = 0
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id
		cart = Cart.objects.get(id=cart_id)
		return cart

	def get(self, request, *args, **kwargs):
		cart = self.get_object()
		delete_item = request.GET.get("delete", False)
		item_id = request.GET.get("item")
		fromcart = request.GET.get("fromcart")
		item_added = False
		if item_id:
			item_instance = get_object_or_404(Product, id=item_id)
			qty = request.GET.get("qty",1)
			print qty
			try:
				if int(qty) < 1:
					delete_item = True
			except:
				raise Http404
			cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
			if created:
				flash_message = "Successfully added to the cart"
				item_added = True
				cart_item.quantity = int(qty)
				cart_item.save()
			if delete_item:
				flash_message = "Item removed successfully."
				cart_item.delete()
			else:
				if not created:
					if fromcart:
						cart_item.quantity = int(qty)
						cart_item.save()
					else:
						cart_item.quantity += int(qty)
						cart_item.save()
					flash_message = "Quantity has been updated successfully."
			if not request.is_ajax():
				return HttpResponseRedirect(reverse("cart"))		
		if request.is_ajax():
			try:
				total = cart_item.line_item_total
			except:
				total = None
			try:
				subtotal = cart_item.cart.subtotal
			except:
				subtotal = None

			try:
				cart_total = cart_item.cart.total
			except:
				cart_total = None

			try:
				total_items = cart_item.cart.items.count()
			except:
				total_items = 0

			data = {
				"deleted": delete_item, 
				"item_added": item_added,
				"line_total": total,
				"subtotal": subtotal,
				"cart_total": cart_total,
				"flash_message": flash_message,
				"total_items": total_items
			}
			return JsonResponse(data) 
		context = {
			"object": self.get_object(),
		}
		template = self.template_name
		return render(request,template,context)