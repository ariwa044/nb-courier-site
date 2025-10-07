from django import forms
from .models import Package, Customer

class TrackingCodeForm(forms.Form):
    tracking_code = forms.CharField(max_length=50, label='Tracking Code')