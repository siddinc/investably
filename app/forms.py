from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import Portfolio, Stock


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()
    #overriding the default field labels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Name'
        self.fields['email'].label = 'Email'

class StockForm(forms.ModelForm):
    class Meta():
        model = Stock
        fields = ("invested_date", "volume")

        widgets = {
            'invested_date': forms.TextInput(attrs = {'class': 'form-control',
                                                        'placeholder': 'YYYY-MM-DD'}),

        }

