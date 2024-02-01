from django.urls import reverse
from django.http import HttpResponsePermanentRedirect

class AddTrailingSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404 and not request.path.endswith('/'):
            new_url = request.path + '/'
            if request.GET:
                new_url += '?' + request.GET.urlencode()
            return HttpResponsePermanentRedirect(new_url)
        return response
