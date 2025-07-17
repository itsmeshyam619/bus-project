# forms.py

from django import forms

class BusSearchForm(forms.Form):
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))


