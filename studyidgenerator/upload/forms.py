import re

from django import forms
from django.core.exceptions import ValidationError

PATTERN = r'\d{8}'
class SeedsForm(forms.Form):
    birthday = forms.CharField(label=(u'Birthday'),
            max_length=8,
    )
    studydate = forms.CharField(label=(u' Study Date'),
            max_length=8,
    )

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if not re.match(PATTERN, birthday):
            raise ValidationError("Birthday is a 8 digits number: yyyymmdd")
        return birthday

    def clean_studydate(self):
        studydate = self.cleaned_data['studydate']
        if not re.match(PATTERN, studydate):
            raise ValidationError("Study Date is a 8 digits number: yyyymmdd")
        return studydate

class UploadForm(forms.Form):
    image = forms.FileField(label="Browse")
