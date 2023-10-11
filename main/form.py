from django import forms
from multiupload.fields import MultiImageField


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileField())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TimeInput(attrs={
        'class': 'form-control',
    }))
    price = forms.FloatField(label='Price', widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))
    image = MultiImageField()
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))
