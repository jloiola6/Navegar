from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import LocationForm, RouteForm, RouteWeekdayFormSet
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
    suppliers = CustomUser.objects.filter(is_superuser= False)

    if request.method == 'POST':
        name = request.POST.get('name')
        supplier = request.POST.get('supplier')

        boat = Boat(name=name, user_id=supplier)
        boat.save()
        
    return render(request, 'route/manage-boats.html', {'suppliers': suppliers})

# def manage_routes(request):
#     return render(request, 'route/manage-routes.html')

def manage_routes(request):
    if request.method == 'POST':
        route_form = RouteForm(request.POST)
        formset = RouteWeekdayFormSet(request.POST)

        if route_form.is_valid() and formset.is_valid():
            route = route_form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.route = route
                instance.save()
            # return redirect('rota-lista')  # Redireciona para a página de listagem de rotas
    else:
        route_form = RouteForm()
        formset = RouteWeekdayFormSet()

    return render(request, 'route/manage-routes.html', {'route_form': route_form, 'formset': formset})