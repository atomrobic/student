from datetime import date
from django import forms
from .models import Student, SupportDocument
from django.core.exceptions import ValidationError

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'email', 'phone', 'dob', 'gender', 'address',
            'latitude', 'longitude', 'course', 'profile_photo'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'max': date.today().strftime('%Y-%m-%d')}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number must be 10 digits.")
        return phone
    


class SupportDocumentForm(forms.Form):
    documents = forms.FileField(required=False)  # remove ClearableFileInput
