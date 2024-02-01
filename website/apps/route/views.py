from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import LocationForm
from .models import Location, Boat
from apps.user.models import CustomUser

# Create your views here.
@login_required
def manage_locations(request):
    locations = Location.objects.all().values_list('name', flat=True)

    form = LocationForm()
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'route/manage-locations.html', {'form': form, 'locations': locations})

def manage_boats(request):
    suppliers = CustomUser.objects.filter(is_superuser= False, type= 'F')
    boats = Boat.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        supplier = request.POST.get('supplier')

        boat = Boat(name=name, user_id=supplier)
        boat.save()
        
    return render(request, 'route/manage-boats.html', {'suppliers': suppliers, "boats": boats})

def manage_routes(request):
    return render(request, 'route/manage-routes.html')