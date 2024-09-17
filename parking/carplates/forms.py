from django import forms


class imageForm(forms.Form):
    image = forms.ImageField()


class plateNumberForm(forms.Form):
    plate_number = forms.CharField(
        max_length=10,
        label='Введіть номер машини',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'AA1234AA'
        })
    )
