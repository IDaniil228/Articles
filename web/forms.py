from django import  forms


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=256)
    surname = forms.CharField(max_length=256)
    login = forms.CharField(max_length=256)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    repetitionPassword = forms.CharField(max_length=256, widget=forms.PasswordInput())
