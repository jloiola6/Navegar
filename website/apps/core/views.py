from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from datetime import datetime



from apps.core.models import *
from apps.route.models import *
from apps.route.utils import find_routes_with_weekday


# Create your views here.

def index(request):      
    template_name = 'index.html'

    origins = Route.objects.values_list('origin', flat=True).order_by('destination').distinct()
    destinations = Route.objects.values_list('destination', flat=True).order_by('destination').distinct()

    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        date = datetime.strptime(request.POST.get('date'), "%Y-%m-%d").date()
        weekday = date.strftime('%A')  # Convert date to weekday

        found_routes = find_routes_with_weekday(origin, destination, weekday)
        if found_routes:
            routes_list = [Route.objects.filter(id__in=routes) for routes in found_routes]

    return TemplateResponse(request, template_name, locals())