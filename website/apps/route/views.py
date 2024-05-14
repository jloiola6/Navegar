from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.db.models.functions import Lower

from .forms import LocationForm, RouteForm, RouteWeekdayFormSet
from .models import Location, Boat, Route, RouteWeekday, WEEKDAYS
from apps.user.models import CustomUser

import re

# Create your views here.

@login_required
def index(request):
    routes = Route.objects.all()

    if request.method == 'POST':
        if request.POST.__contains__('switch_discount'):
            route_id = request.POST.get('switch_discount')
            route = Route.objects.get(id= route_id)
            route.switch_discount()

    return render(request, 'route/index.html', {'routes': routes})

@login_required
def locations(request):
    locations = Location.objects.all().order_by(Lower('name'))

    form = LocationForm()
    if request.method == 'POST':
        if request.POST.__contains__('location_id'):
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
        else:
            messages.error(request, 'Este local já existe, tente novamente')

            return redirect(reverse('route:locations'))

    return render(request, 'route/locations.html', {
        'form': form, 
        'locations': locations
    })

@login_required
def boats(request):
    suppliers = CustomUser.objects.filter(is_superuser= False, type= 'F').order_by('full_name')
    boats = Boat.objects.all().order_by(Lower('name'))

    if request.method == 'POST':
        name = request.POST.get('name')
        supplier = request.POST.get('supplier')

        if request.POST.__contains__('boat_id'):
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
def add_route(request):
    template_name = 'route/add-route.html'

    boats = Boat.objects.all()

    route_form = RouteForm(label_suffix="")

    if request.method == 'POST':
        route_form = RouteForm(request.POST)

        if route_form.is_valid():
            route = route_form.save()

            for item in request.POST.items():
                if 'new-weekday' in item[0]:
                    selection_index = re.findall(r"\d+", item[0])[0]

                    boat_id = request.POST[f'new-boat-{selection_index}']
                    boat = Boat.objects.get(id= boat_id)
                    
                    route_weekday = RouteWeekday()

                    route_weekday.route = route
                    route_weekday.boat = boat
                    route_weekday.weekday = item[1]
                    
                    route_weekday.save()
                    
            return redirect(reverse('route:index'))
          
    return render(request, template_name, {
        'boats': boats, 
        'route_form': route_form,
        'WEEKDAYS': WEEKDAYS 
    })

@login_required
def edit_route(request, route_id):
    template_name = 'route/edit-route.html'

    route = Route.objects.get(id= route_id)

    route_form = RouteForm(instance= route, label_suffix="")

    route_weekdays = RouteWeekday.objects.filter(route= route)
    route_boats = route_weekdays.values('boat', 'boat__name').distinct()

    boats = Boat.objects.all()

    for boat in route_boats:
        boat['weekdays'] = route_weekdays.filter(boat= boat['boat']).values_list('weekday', flat= True)

    if request.POST:
        route_form = RouteForm(request.POST, instance= route)

        if route_form.is_valid():
            route = route_form.save()

            route_weekdays = RouteWeekday.objects.filter(route= route)

            for route_weekday in route_weekdays:
                boat = route_weekday.boat
                weekday = route_weekday.weekday

                remove_route_weekday = True

                for item in request.POST.items():
                    if f'boat-{boat.id}-weekday' in item[0] and weekday == item[1]:
                        remove_route_weekday = False

                if remove_route_weekday:
                    route_weekday.delete()

            for item in request.POST.items():
                if 'boat' in item[0] and 'weekday' in item[0] and not 'new' in item[0]:
                    boat_id = item[0].split('-')[1]
                    boat = boats.get(id= boat_id)


                    if not route_weekdays.filter(route= route, boat= boat, weekday= item[1]).exists():
                        route_weekday = RouteWeekday()
                        route_weekday.route = route
                        route_weekday.boat = boat
                        route_weekday.weekday = item[1]
                        
                        route_weekday.save()

                elif 'weekday' in item[0] and'new' in item[0]:
                    selection_index = item[0].split('-')[2]
                    boat_id = request.POST[f'new-boat-{selection_index}']
                    boat = boats.get(id= boat_id)

                    route_weekday = RouteWeekday()
                    route_weekday.route = route
                    route_weekday.boat = boat
                    route_weekday.weekday = item[1]
                    route_weekday.save()

            messages.success(request, 'Rota editada com sucesso!')
            
            return redirect(reverse(f'route:edit-route', args=[route.id]))

    return render(request, template_name, {
        'boats': boats,
        'route_form': route_form,
        'route_weekdays': route_weekdays,
        'route_boats': route_boats,
        'WEEKDAYS': WEEKDAYS
    })