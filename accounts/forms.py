from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Team
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email") 

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  
        widget=forms.CheckboxSelectMultiple,
        label="Ekip Üyeleri"
    )

    class Meta:
        model = Team
        fields = ['name', 'members'] 

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)  
        super().__init__(*args, **kwargs)
        if current_user:
            self.fields['members'].queryset = User.objects.exclude(id=current_user.id)
        else:
            self.fields['members'].queryset = User.objects.all()