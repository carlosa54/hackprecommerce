from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from django.views.generic import CreateView

# Create your views here.
def home(request):
	return redirect('products')

class ProductListView(ListView):
	model = Product

class ProductDetailView(DetailView):
	model = Product