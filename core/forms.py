from django import forms


class FlightSearchForm(forms.Form):
    src = forms.CharField(max_length=3)
    dst = forms.CharField(max_length=3)
    date_from = forms.DateField(input_formats=['%d/%m/%Y'])
    date_to = forms.DateField(input_formats=['%d/%m/%Y'])
