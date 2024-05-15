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

        if request.POST.__contains__('voucher'):
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
    from django.conf import settings 

    ticket_type = request.GET.get('tipo')
    choose_type = ticket_type == None

    route_weekday = RouteWeekday.objects.get(id=id)

    if request.method == 'POST':
        if ticket_type == 'passageiro':
            error_message = True

            for item in request.POST.items():
                if 'client' in item[0]:
                    error_message = False

                    client_index = item[0].split('_')[1]
                    client_name = item[1]

                    birth_date = request.POST[f'birth_date_{ client_index }'] or None
                    document_type = request.POST[f'document_type_{ client_index }']
                    document = request.POST[f'document_{ client_index }']

                    ticket = Ticket.objects.create(
                        user_create = request.user,
                        route_weekday = route_weekday,
                        type = ticket_type,

                        origin = route_weekday.route.origin.name,
                        destination = route_weekday.route.destination.name,
                        date = date,
                        boat = route_weekday.boat.name,

                        value = route_weekday.get_value,
                        cost = route_weekday.get_cost,

                        name_client = client_name,
                        document_client = document,
                        document_type = document_type,
                        birth_date_client = birth_date
                    )

                    message = f'''NOVA PASSAGEM
{ticket.origin} - {ticket.destination}
{ticket.date}
Embarcação: {ticket.boat}

Passageiro: {client_name}
Identificação ({document_type}): {document}
Nascimento: {birth_date}'''
                    ticket.send_message(ticket.supplier.phone, message)

            if error_message:
                messages.error(request, 'Adicione pelo menos um passageiro')
                return redirect(f'/passagens/adicionar/{id}/{date}?tipo={ticket_type}')
        
        else:
            cargo_description = request.POST['cargo_description']
            cargo_weight = request.POST['cargo_weight'] or None

            ticket = Ticket.objects.create(
                user_create = request.user,
                route_weekday = route_weekday,
                type = ticket_type,

                origin = route_weekday.route.origin.name,
                destination = route_weekday.route.destination.name,
                date = date,
                boat = route_weekday.boat.name,

                value = route_weekday.get_value,
                cost = route_weekday.get_cost,

                cargo_description = cargo_description,
                cargo_weight = cargo_weight
            )
            message = f'''NOVA PASSAGEM
{ticket.origin} - {ticket.destination}
{ticket.date}
Embarcação: {ticket.boat}

Descrição: {ticket.cargo_description}
Peso:{ticket.cargo_weight}'''
            ticket.send_message(ticket.supplier.phone, message)

        return redirect(reverse('ticket:index'))

    return render(request, 'ticket/add.html', {
        'choose_type': choose_type,
        'date': date,
        'routeweek': route_weekday,
        'ticket_type': ticket_type,
    })

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