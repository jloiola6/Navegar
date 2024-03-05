from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.ticket.models import *
from apps.ticket.forms import TicketForm
from apps.route.models import RouteWeekday
from apps.core.models import Utils


@login_required
def index(request):
    tickets = Ticket.objects.all().order_by('status', '-date')

    return render(request, 'ticket/index.html', {'tickets': tickets})

@login_required
def add(request, id, date):
    routeweek = RouteWeekday.objects.get(id=id)

    return render(request, 'ticket/add.html', {'routeweek': routeweek, 'date': date})

@login_required
def create_ticket(request, id, date):
    if request.method == 'POST':
        routeweek = RouteWeekday.objects.get(id=id)

        if Utils.objects.all().exists():
            utils = Utils.objects.first()
        else:
            utils = Utils.objects.create()

        client = request.POST['client']
        document = request.POST['document']
        birth_date = request.POST['birth-date']

        ticket = Ticket.objects.create(
            user_create = request.user,
            route_weekday = routeweek,
            date = date,
            name_client = client,
            docuemnt_client = document,
            birth_date_client = birth_date,
            value = routeweek.route.discounted_value if utils.discount else routeweek.route.value,
            origin = routeweek.route.origin.name,
            destination = routeweek.route.destination.name,
            boat = routeweek.boat.name
        )
        ticket.save()
        
        return redirect(reverse('ticket:index'))

@login_required
def edit(request):
    return render(request, 'ticket/edit.html')

@login_required
def view(request, pk):
    ticket = Ticket.objects.get(id=pk)
    routeweek = ticket.route_weekday

    form = TicketForm(instance=ticket)

    if request.method == 'POST':
        if request.POST.get('voucher'):
            ticket.update_status(2)
            messages.success(request, 'Voucher emitido com sucesso')
        
            return redirect(reverse('ticket:view', args=[ticket.id]))

        form = TicketForm(request.POST, request.FILES, instance=ticket)
        
        if form.is_valid():
            form.save()
            ticket.update_status(2)
            messages.success(request, 'Bilhete enviado com sucesso')
            
            return redirect(reverse('ticket:view', args=[ticket.id]))

    return render(request, 'ticket/view.html', {'ticket': ticket, 'routeweek': routeweek, 'form': form})

@login_required
def print(request, id):
    ticket = Ticket.objects.get(id= id)
    routeweek = ticket.route_weekday

    return render(request, 'ticket/print.html', {
        'ticket': ticket,
        'routeweek': routeweek
    })