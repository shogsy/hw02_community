from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .validators import validate_not_empty

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, validators=[validate_not_empty])
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
