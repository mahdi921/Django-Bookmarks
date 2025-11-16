from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from account.models import Profile


User = get_user_model()


class EditProfileForm(forms.ModelForm):
    '''
    Custom form to use for editing user profile info
    '''
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name',
            'username', 'date_of_birth',
            'bio', 'photo'
        ]


class EditUserForm(forms.ModelForm):
    '''
    Custom form to use for editing user profile info
    '''
    class Meta:
        model = User
        fields = [
            'email'
        ]
        

class UserRegistrationForm(UserCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
