from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.ticket.models import *
from apps.ticket.forms import TicketForm
from apps.route.models import RouteWeekday

@login_required
def index(request):
    pending_tickets = Ticket.objects.filter(status= 1).order_by('created_at')
    available_tickets = Ticket.objects.filter(status= 4).order_by('-created_at')

    if request.method == 'POST':
        ticket_id = request.POST['ticket_id']
        ticket = Ticket.objects.get(id= ticket_id)

        if request.POST.get('voucher'):
            ticket.update_status(4)
            messages.success(request, 'Voucher emitido com sucesso!')

            return redirect(reverse('ticket:index'))
        
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        
        if form.is_valid():
            form.save()
            ticket.update_status(4)
            messages.success(request, 'Bilhete enviado com sucesso')
            
            return redirect(reverse('ticket:index'))

    return render(request, 'ticket/index.html', {
        'pending_tickets': pending_tickets,
        'available_tickets': available_tickets
    })

@login_required
def add(request, id, date):
    routeweek = RouteWeekday.objects.get(id=id)

    return render(request, 'ticket/add.html', {
        'date': date,
        'routeweek': routeweek,
    })

@login_required
def create_ticket(request, id, date):
    if request.method == 'POST':
        routeweek = RouteWeekday.objects.get(id=id)

        client = request.POST['client']
        document = request.POST['document']
        document_type = request.POST['document_type']
        birth_date = request.POST['birth-date']
        markdown = request.POST.get('markdown') == 'on'

        ticket = Ticket.objects.create(
            user_create = request.user,
            route_weekday = routeweek,
            date = date,
            name_client = client,
            document_client = document,
            document_type = document_type,
            birth_date_client = birth_date,
            value = routeweek.route.get_value,
            cost = routeweek.route.get_cost,
            origin = routeweek.route.origin.name,
            destination = routeweek.route.destination.name,
            boat = routeweek.boat.name,
            markdown = markdown
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
        if request.POST.__contains__('cancelled'):
            ticket.update_status(5)

            if ticket.is_upload:
                messages.info(request, 'Bilhete cancelado')
            else:
                messages.info(request, 'Voucher cancelado')

        if request.POST.__contains__('refused'):
            ticket.update_status(3)
            messages.info(request, 'Solicitação recusada')

            return redirect(reverse('ticket:view', args=[ticket.id]))
        
        if request.POST.__contains__('no_show'):
            ticket.update_status(7)
            messages.info(request, 'Não comaprecimento informado')

            return redirect(reverse('ticket:view', args=[ticket.id]))

        if request.POST.__contains__('order_cancellation'):
            ticket.update_status(2)
            messages.info(request, 'Solicitação cancelada')

            return redirect(reverse('ticket:view', args=[ticket.id]))

        if request.POST.__contains__('voucher'):
            ticket.update_status(4)
            messages.success(request, 'Voucher emitido com sucesso')
        
            return redirect(reverse('ticket:view', args=[ticket.id]))
        
        if request.FILES.get('document'):
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            
            if form.is_valid():
                form.save()
                ticket.update_status(4)
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