from django.shortcuts import render

from upload.models import Image

def index(request):
    result = Image.objects.all()
    print dir(result)
    context = {'result': result}
    template = 'download_page.html'
    return render(request, template, context)
