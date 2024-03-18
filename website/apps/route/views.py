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
def locations(request):
    locations = Location.objects.all().order_by(Lower('name'))

    form = LocationForm()
    if request.method == 'POST':
        if request.POST.get('location_id'):
            location_id = request.POST.get('location_id')
            name = request.POST.get('name')

            location = Location.objects.get(id= location_id)

            location.name = name
            location.save()

            messages.success(request, 'Local atualizado')

            return redirect(reverse('route:locations'))

        form = LocationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Local cadastrado')

            return redirect(reverse('route:locations'))

    return render(request, 'route/locations.html', {
        'form': form, 
        'locations': locations
    })

@login_required
def boats(request):
    suppliers = CustomUser.objects.filter(is_superuser= False, type= 'F')
    boats = Boat.objects.all().order_by(Lower('name'))

    if request.method == 'POST':
        name = request.POST.get('name')
        supplier = request.POST.get('supplier')

        if request.POST.get('boat_id'):
            boat = Boat.objects.get(id= request.POST.get('boat_id'))
            boat.name = name
            boat.supplier = CustomUser.objects.get(id= supplier)

            boat.save()
            messages.success(request, 'Embarcação atualizada')

            return render(request, 'route/boats.html', {'suppliers': suppliers, "boats": boats})

        boat = Boat(name=name, supplier_id=supplier)
        boat.save()

        messages.success(request, 'Embarcação cadastrada')
        
    return render(request, 'route/boats.html', {'suppliers': suppliers, "boats": boats})

@login_required
def add_route(request, route_id=None):
    template_name = 'route/add-route.html'

    if route_id:
        route = Route.objects.get(id=route_id)
        route_form = RouteForm(instance=route, label_suffix="")
        formset = RouteWeekdayFormSet(instance=route)
        template_name = 'route/edit-route.html'
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
            return redirect(reverse('route:index'))
          
    return render(request, template_name, {'route_form': route_form, 'formset': formset})