from django.shortcuts import render, redirect
from django.urls import reverse

from apps.ticket.models import *
from apps.user.models import CustomUser



def create_ticket(request):
    if request.method == 'POST':
        ticket = Ticket.objects.create(
            user = request.user,
            origin = request.POST['origin'],
            destination = request.POST['destination'],
            date = request.POST['date'],
            boat = request.POST['boat'],
            value = request.POST['value'],
            status = request.POST['status']
        )
        return redirect(reverse('core:index'))