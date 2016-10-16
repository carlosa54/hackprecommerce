from django.conf.urls import url
from .views import ATHMovilCheckoutView

urlpatterns = [
	url(r'^$', ATHMovilCheckoutView.as_view(), name='athmovil'),
]