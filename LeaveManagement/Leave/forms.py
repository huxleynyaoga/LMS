from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from .models import LeaveApplication



# - Login Form

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    
# - Leave Application Form

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = [
            'leave_type',
            'start_date',
            'end_date',
            'reason',
            'total_leave_days',
            'officer_handing_over_duty_to',
            'supervisor_name',
            'department',
        ]
        labels = {
            'leave_type': 'Type of Leave',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'reason': 'Reason for Leave',
            'total_leave_days': 'Total Leave Days',
            'officer_handing_over_duty_to': 'Handing Duties To',
            'supervisor_name': 'Supervisor Name',
            'department':'Department',
        }
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'start_date', 'type': 'date', 'autocomplete': 'off'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'end_date', 'type': 'date', 'autocomplete': 'off'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'total_leave_days': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'readonly': 'readonly'}),
            'officer_handing_over_duty_to': forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'supervisor_name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }