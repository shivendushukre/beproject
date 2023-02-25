from django import forms

class UploadPaperForm(forms.Form):
    file = forms.FileField()