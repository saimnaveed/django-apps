from django.shortcuts import render, HttpResponse
from datetime import datetime
from first_mango.models import contact
from django.contrib import messages

# Create your views here.
def index(request):
    context= {'variable1':"Chaunsa the great",
              'variable2':"Dusehri"}
    #return HttpResponse("My First Webpage.")

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')
    #return HttpResponse("My First About Webpage.")

def services(request):
    return render(request, 'services.html')
    #return HttpResponse("My First Services Webpage.")

def contacts(request):
    if request.method == "POST":
        namee = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')
        #date = request.POST.get('name')
        
        contact_form = contact(name=namee,email=email,phone=phone, description=description, date=datetime.today())
        contact_form.save()
        messages.success(request, 'Response submitted')
    return render(request, 'contacts.html')
    #return HttpResponse("My First Contact Webpage.")

def groupinformatics(request):
    return render(request, 'groupinformatics.html')
def datascience(request):
    return render(request, 'datascience.html')

def blockchain(request):
    return render(request, 'blockchain.html')

def infrastructure_security(request):
    return render(request, 'infrastructure_security.html')