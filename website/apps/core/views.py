from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from datetime import datetime



from apps.core.models import *
from apps.route.models import *
from apps.route.utils import find_routes_with_weekday
from apps.route.models import Route
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def index(request):      
    template_name = 'route/index.html'

    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        date = datetime.strptime(request.POST.get('date'), "%Y-%m-%d").date()
        weekday = date.strftime('%A')  # Convert date to weekday

        # found_routes = find_routes_with_weekday(origin, destination, weekday)
        # if found_routes:
        #     routes_list = [Route.objects.filter(id__in=routes) for routes in found_routes]

        # routes_list = Route.objects.filter(origin=origin, destination=destination, weekday=weekday)

    return TemplateResponse(request, template_name, locals())