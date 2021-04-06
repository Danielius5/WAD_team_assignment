from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment,Rating

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


class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields =('user','book','comment')


class RatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields = ('user','book','rating')


