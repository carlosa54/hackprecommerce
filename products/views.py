from django.shortcuts import render

# Create your views here.
def home(request):
	
	context = {
		"test" : "Testing home",
	}
	return render(request, "home.html", context)