import datetime
import hashlib
import os
import shutil
import zipfile

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.files.temp import NamedTemporaryFile

from .forms import SeedsForm, UploadForm
from .models import Image
from .code.anonymizer import Anonymize
from django.conf import settings

@login_required
def index(request):
    form = SeedsForm(request.POST or None)
    template = "upload_index.html"
    context = {'form': form}
    if form.is_valid():
        birthday = form.clean_birthday()
        studydate = form.clean_studydate()
        hash_value = _create_id(birthday, studydate)
        user = request.user
        studyid_query = Image.objects.all().filter(owner=user,
                studyid=hash_value)
        if studyid_query:
            return HttpResponse('<html><body><h2>Deu Merda</h2></body></html>')
        image_form = UploadForm()
        template = 'generate_page.html'
        context = {'hash_value': hash_value, 'upload_form': image_form}
    return render(request, template, context)

@login_required
def success(request):
    if request.method == 'GET':
        return HttpResponseRedirect("/upload/")
    upload_form = UploadForm(request.POST, request.FILES)
    user = request.user
    template = 'generate_page.html'
    context = {'user': user, 'upload_form': upload_form}
    if upload_form.is_valid():
        error_dict, studyid = handle_uploaded_file(request)
        if  error_dict['anonymized']:
            template = 'upload_error.html'
            context = {'user': request.user, 'error': 'NotAnonymized'}
            return render(request, template, context)
        elif not error_dict['onepatient']:
            template = 'upload_error.html'
            context = {'user': request.user, 'error': 'OnePatient'}
            return render(request, template, context)

        newimage = Image(owner=user, image=request.FILES['image'],
                studyid=studyid,
                date=datetime.datetime.now()
        )
        newimage.save()
        template = 'success_page.html'
    return render(request, template, context)

def _create_id(birthday, studydate):
    return str(hashlib.sha224(birthday + studydate).hexdigest()[0:10])

def handle_uploaded_file(request):
    anonymous = Anonymize(silent=True)
    dicom_names, temp_dir = create_temp_file(request)
    dicom_files = anonymous.open_dicom_files(dicom_names)
    shutil.rmtree(temp_dir)
    one_patient = anonymous.is_one_patient(dicom_files)
    is_anonymized = anonymous.is_anonymized(dicom_files)
    studyid = anonymous.get_studyid(dicom_files[0])
    print studyid
    error_dict = {'anonymized': is_anonymized, 'onepatient': one_patient}
    return error_dict, studyid

def create_temp_file(request):
    """
        Crate a temporary file for data validation
    """
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'tempdir')
    try:
        os.mkdir(temp_dir)
    except:
        pass
    temp_file_path = os.path.join(temp_dir, 'tempfile.zip')

    data = request.FILES['image']
    output = open(temp_file_path, 'wb')
    for chunk in data.chunks():
        output.write(chunk)
    output.close()
    dicom_names = open_zip(temp_dir, temp_file_path)
    return dicom_names, temp_dir

def open_zip(temp_dir, file_path):
    zip_file = zipfile.ZipFile(file_path)
    dicom_names = []
    for name in zip_file.namelist():
        if name.endswith(".dcm") and not name.startswith('__'):
            dicom_name = os.path.join(temp_dir, name)
            outfile = open(dicom_name, 'wb')
            outfile.write(zip_file.read(name))
            outfile.close()
            dicom_names.append(dicom_name)
    return dicom_names

