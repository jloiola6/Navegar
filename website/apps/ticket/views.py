from django.shortcuts import render, redirect
from django.urls import reverse

from apps.ticket.models import *
from apps.user.models import CustomUser
from apps.route.models import RouteWeekday

def index(request):
    return render(request, 'tickets/index.html')

def add(request, id, date):
    routeweek = RouteWeekday.objects.get(id=id)

    return render(request, 'tickets/add.html', {'routeweek': routeweek, 'date': date})

def create_ticket(request, id, date):
    if request.method == 'POST':
        routeweek = RouteWeekday.objects.get(id=id)

        client = request.POST['client']
        document = request.POST['document']

        ticket = Ticket.objects.create(
            user_create = request.user,
            route_weekday = routeweek,
            date = date,
            name_client = client,
            docuemnt_client = document,
        )
        ticket.save()
        
        return redirect(reverse('core:index'))