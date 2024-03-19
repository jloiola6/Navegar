from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Sum

from apps.ticket.models import Ticket

@login_required
def index(request):
    current_date = datetime.now().date()
    tickets = Ticket.objects.filter(created_at__date= current_date)

    if request.method == 'POST':
        searched_date = request.POST.get('date')
        tickets = Ticket.objects.filter(created_at__date= searched_date)

    total_cost = tickets.aggregate(Sum('cost'))['cost__sum']
    total_value = tickets.aggregate(Sum('value'))['value__sum']

    total_profit = total_value - total_cost

    return TemplateResponse(request, 'financial/index.html', locals())