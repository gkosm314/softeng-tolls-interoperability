from django import forms

#Class that defines the Django form that we will use
class UploadFileForm(forms.Form):
    file = forms.FileField()