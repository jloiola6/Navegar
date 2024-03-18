from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from apps.ticket.models import Ticket

@login_required
def index(request):
    current_date = datetime.now().date()
    tickets = Ticket.objects.filter(created_at__date= current_date)

    if request.method == 'POST':
        searched_date = request.POST.get('date')
        tickets = Ticket.objects.filter(created_at__date= searched_date)

    return TemplateResponse(request, 'financial/index.html', locals())