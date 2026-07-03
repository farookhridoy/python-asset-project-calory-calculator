from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CalorieProfile, FoodEntry

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CalorieProfile
        fields = ['name', 'age', 'gender', 'height', 'weight']
        widgets = {
            'gender': forms.Select(choices=CalorieProfile.GENDER_CHOICES),
        }

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ['item_name', 'calories']
