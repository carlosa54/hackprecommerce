from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product

# Create your views here.
def home(request):
	
	context = {
		"test" : "Testing home",
	}
	return render(request, "home.html", context)

class ProductListView(ListView):
	model = Product

class ProductDetailView(DetailView):
	model = Product