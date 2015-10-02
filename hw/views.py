from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("<b>Welcome to jacket's world, happy everyday.</b>")

