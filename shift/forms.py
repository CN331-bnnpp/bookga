from django import forms
from .models import Shift

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['start_time', 'num_hours', 'num_people']
        labels = {
            'start_time': 'Start time',
            'num_hours': 'Number of hours',
            'num_people': 'Number of people',
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type':'datetime-local'}),
            'num_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_people': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def save(self, commit=True):
        shift = super(ShiftForm, self).save(commit=False)
        if commit:
            shift.save()
        return shift