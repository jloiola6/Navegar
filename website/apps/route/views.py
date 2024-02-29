from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import LocationForm, RouteForm, RouteWeekdayFormSet
from .models import Location, Boat, Route
from apps.user.models import CustomUser
from apps.core.models import Utils

# Create your views here.
@login_required
def manage_locations(request):
    locations = Location.objects.all().values_list('name', flat=True)

    form = LocationForm()
    if request.method == 'POST':
        form = LocationForm(request.POST)

        if form.is_valid():
            form.save()
            
            return redirect(reverse('route:manage-locations'))

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
    routes = Route.objects.all()
    
    if not Utils.objects.all().exists():
        utils = Utils.objects.get(id=1)
    else:
        utils = Utils.objects.create()
    discount = utils.discount

    if request.method == 'POST':
        if request.POST.get('discount'):
            value = discount
            utils.discount = not value
            utils.save()

    return render(request, 'route/manage-routes.html', {'routes': routes, 'discount': discount})

def add_route(request, route_id=None):
    if route_id:
        route = Route.objects.get(id=route_id)
        route_form = RouteForm(instance=route)
        formset = RouteWeekdayFormSet(instance=route)
    else:
        route_form = RouteForm()
        formset = RouteWeekdayFormSet()


    if request.method == 'POST':
        if route_id:
            route_form = RouteForm(request.POST, instance=route, user=request.user)
            formset = RouteWeekdayFormSet(request.POST, instance=route, user=request.user)
        else:
            route_form = RouteForm(request.POST, user=request.user)
            formset = RouteWeekdayFormSet(request.POST, user=request.user)

        if route_form.is_valid() and formset.is_valid():
            route = route_form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.route = route
                instance.save()
            return redirect(reverse('route:manage-routes'))
          
    return render(request, 'route/add-routes.html', {'route_form': route_form, 'formset': formset})