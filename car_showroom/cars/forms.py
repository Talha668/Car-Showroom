from django import forms
from .models import Inquiry, TestDrive


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message', 'preferred_contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': '4'}),
            'preferred_contact': forms.Select(attrs={'class': 'form-control'}),
        }


class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDrive
        fields = ['name', 'email', 'phone', 'preferred_date', 'preferred_time', 'message']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'prefered_time': forms.TimeInput(attrs={'typr': 'time', 'class': 'form-control'}),
        }        