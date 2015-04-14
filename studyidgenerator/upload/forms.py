from django import forms

class SeedsForm(forms.Form):
    birthday = forms.CharField(label=(u'Birthday'),
            max_length=8,
    )
    studydate = forms.CharField(label=(u' Study Date'),
            max_length=8,
    )


class UploadForm(forms.Form):
    image = forms.FileField(
            label='Select ZIP file',
    )
