from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.db.models.functions import Lower

from .forms import LocationForm, RouteForm, RouteWeekdayFormSet
from .models import Location, Boat, Route
from apps.user.models import CustomUser

# Create your views here.

@login_required
def index(request):
    routes = Route.objects.all()

    if request.method == 'POST':
        if request.POST.get('switch_discount'):
            route_id = request.POST.get('switch_discount')
            route = Route.objects.get(id= route_id)
            route.switch_discount()

    return render(request, 'route/index.html', {'routes': routes})

@login_required
def manage_locations(request):
    locations = Location.objects.all().values_list('name', flat=True).order_by(Lower('name'))

    form = LocationForm()
    if request.method == 'POST':
        form = LocationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Local cadastrado com sucesso')

            return redirect(reverse('route:manage-locations'))

    return render(request, 'route/manage-locations.html', {'form': form, 'locations': locations})

@login_required
def manage_boats(request):
    suppliers = CustomUser.objects.filter(is_superuser= False, type= 'F')
    boats = Boat.objects.all().order_by(Lower('name'))

    if request.method == 'POST':
        name = request.POST.get('name')
        supplier = request.POST.get('supplier')

        boat = Boat(name=name, user_id=supplier)
        boat.save()

        messages.success(request, 'Embarcação cadastrada com sucesso')
        
    return render(request, 'route/manage-boats.html', {'suppliers': suppliers, "boats": boats})

@login_required
def add_route(request, route_id=None):
    if route_id:
        route = Route.objects.get(id=route_id)
        route_form = RouteForm(instance=route, label_suffix="")
        formset = RouteWeekdayFormSet(instance=route)
    else:
        route_form = RouteForm(label_suffix="")
        formset = RouteWeekdayFormSet()

    if request.method == 'POST':
        if route_id:
            route_form = RouteForm(request.POST, instance=route)
            formset = RouteWeekdayFormSet(request.POST, instance=route)
        else:
            route_form = RouteForm(request.POST)
            formset = RouteWeekdayFormSet(request.POST)

        if route_form.is_valid() and formset.is_valid():
            route = route_form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.route = route
                instance.save()
            return redirect(reverse('route:manage-routes'))
          
    return render(request, 'route/add-routes.html', {'route_form': route_form, 'formset': formset})