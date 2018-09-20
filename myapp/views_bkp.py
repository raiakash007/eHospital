from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def patientSignup(request):
    return render(request,'patientSignup.html')
