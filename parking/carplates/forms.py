from django import forms


class imageForm(forms.Form):
    image = forms.ImageField()
