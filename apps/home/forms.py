"""Forms for home app."""
from django import forms
from apps import constants as con


class ScrapSearchForm(forms.Form):
    """Search form for scraping."""

    search_item = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required': True})
    )
    site_choice = forms.ChoiceField(
        required=True, choices=con.SITE_CHOICES,
        widget=forms.RadioSelect(attrs={'required': True}))


class DashboardSearchForm(forms.Form):
    """Search products from database."""

    search_item = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required': True}
        )
    )
