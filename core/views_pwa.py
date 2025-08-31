from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage

def service_worker(request):
    js = staticfiles_storage.open('pwa/service-worker.js').read()
    return HttpResponse(js, content_type='application/javascript')

def manifest(request):
    data = staticfiles_storage.open('pwa/manifest.json').read()
    return HttpResponse(data, content_type='application/manifest+json')
