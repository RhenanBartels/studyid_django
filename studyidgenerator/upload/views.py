import hashlib

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SeedsForm, UploadForm
from .models import Image

@login_required
def index(request):
    form = SeedsForm(request.POST or None)
    template = "upload_index.html"
    context = {'form': form}
    if form.is_valid():
        image_form = UploadForm()
        template = 'generate_page.html'
        birthday = form.cleaned_data['birthday']
        studydate = form.cleaned_data['studydate']
        hash_value = _create_id(birthday, studydate)
        context = {'hash_value': hash_value, 'upload_form': image_form}
    return render(request, template, context)

@login_required
def success(request):
    upload_form = UploadForm(request.POST, request.FILES)
    template = 'generate_page.html'
    context = {'upload_form': upload_form}
    user = request.user
    if upload_form.is_valid():
        newimage = Image(owner=user, image=request.FILES['image'],
                studyid='12345678',
                date='2015-12-12'
        )
        newimage.save()
        template = 'success_page.html'
    return render(request, template, context)
#@login_required
#def generate(request):
#    form = SeedsForm(request.POST or None)
#    if form.is_valid():
#        print form.cleaned_data['birthday']
#    context = {'hash_value': '12455676'}
#    template = 'generate_page.html'
#    return render(request, template, context)


def _create_id(birthday, studydate):
    return str(hashlib.sha224(birthday + studydate).hexdigest()[0:11])
