from django import  forms

from web.models import Articles


import datetime

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=256)
    surname = forms.CharField(max_length=256)
    login = forms.CharField(max_length=256)
    photo = forms.ImageField()
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())
    repetitionPassword = forms.CharField(max_length=256, widget=forms.PasswordInput())


class AuthorizationForm(forms.Form):
    login = forms.CharField(max_length=256)
    password = forms.CharField(max_length=256, widget=forms.PasswordInput())

class ArticlesForm(forms.ModelForm):

    def save(self, commit=True):
        self.instance.create_data = datetime.date.today()
        self.instance.user = self.initial["user"]
        return super().save(commit)

    class Meta:
        model = Articles
        fields = ["title", "content", "image"]
        widgets = {
            "content" : forms.Textarea(attrs={"cols" : 60, "row": 10}),
        }