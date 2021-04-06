from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from booklists.models import *
from django import forms

class UserForm(UserCreationForm):
    #email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields=('username','password1','password2')

    def save(self,commit=True):
        user=super(UserForm,self).save(commit=False)
        #user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ListForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    is_public = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = List
        fields = ('name', 'is_public')