from django.conf.urls import url
from .views import ATHMovilCheckoutView,PaymentList

urlpatterns = [
	url(r'^$', ATHMovilCheckoutView.as_view(), name='athmovil'),
	url(r'^payments/$', PaymentList.as_view(), name='payments'),
]