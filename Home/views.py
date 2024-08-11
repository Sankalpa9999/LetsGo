from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from .models import ContactMessage
# Create your views here.

def index(request):
    return render (request,'Home/index.html')

def about(request):
    return render(request,'Home/about.html')

def facilities(request):
    return render(request,'Home/facilities.html')


from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from .models import ContactMessage

def contact_view(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the data to the model
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                mobile=form.cleaned_data['mobile'],
                address=form.cleaned_data['address'],
                message=form.cleaned_data['message']
            )
            success = True  # Set the success flag to True
    else:
        form = ContactForm()

    return render(request, 'Home/contact.html', {'form': form, 'success': success})

