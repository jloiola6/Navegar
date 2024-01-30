from django.shortcuts import render

# Create your views here.
def manage_locations(request):
    return render(request, 'route/manage-locations.html')

def manage_boats(request):
    return render(request, 'route/manage-boats.html')

def manage_routes(request):
    return render(request, 'route/manage-routes.html')