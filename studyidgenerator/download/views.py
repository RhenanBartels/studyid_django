import os
from StringIO import StringIO

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from upload.models import Image

@login_required
def index(request):
    user = request.user
    try:
        result = Image.objects.all().filter(owner_id=user.id)
    except Image.DoesNotExist:
        result = None
    if not result.count():
        result = None
    context = {'result': result}
    template = 'download_page.html'
    return render(request, template, context)

@login_required
def download_media(request, studyid):
    user =  request.user
    result = Image.objects.get(owner=user, studyid=studyid)
    image = StringIO(file(result.image.path, "rb").read())
    return HttpResponse(image.read(), content_type='application/zip')
