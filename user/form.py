from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username' : TextInput(attrs={'class':'input', 'placeholder':'username'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'}),
        }
UNIVERSITY = [
    ('Karabük', 'Karabük'),
    ('İTÜ', 'İTÜ'),
    ('KTü', 'KTÜ'),
    ('ODTÜ','ODTÜ'),
]
FACULTY = [
    ('Mühendislik', 'Mühendislik'),
    ('İşletme','İşletme'),
    ('İlahiyat','İşletme'),
    ('Fen','Fen'),
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone','university','faculty','image')
        widgets = {
            'phone' : TextInput(attrs={'class':'input', 'placeholder':'phone'}),
            'university' : Select(attrs={'class':'input', 'placeholder': 'university'},choices=UNIVERSITY),
            'faculty': Select(attrs={'class':'input', 'placeholder': 'faculty'},choices=FACULTY),
            'image': FileInput(attrs={'class':'input','placeholder':'image'}),
        }