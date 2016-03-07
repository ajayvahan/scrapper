"""Forms for home app.

It contains search form for scap and dashboard page.
"""
from django import forms
from apps import constants as con


class ScrapSearchForm(forms.Form):
    """Search form for scraping.

    It provide all the fields needed for search form.
    """

    # Textbox fields.
    search_item = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'required': True, 'autofocus': True,
                'placeholder': 'Scrap here'}))

    # Radio fields.
    site_choice = forms.ChoiceField(
        required=True, choices=con.SITE_CHOICES,
        widget=forms.RadioSelect(attrs={'required': True}))


class DashboardSearchForm(forms.Form):
    """Search products from database.

    It provide all the fields needed for search form.
    """

    # Textbox fields.
    search_item = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'required': True, 'autofocus': True,
                'placeholder': 'What would you like to search?'}))


class DashboardFilterForm(forms.Form):
    """Search products from database.

    It provide all the fields needed for search form.
    """

    # Radio fields.
    price_sort = forms.ChoiceField(
        required=False, choices=con.PRICE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'filter-click',
                                        'required': False}))

    # Checkbox fields.
    amazon = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'filter-click'}))
    flipkart = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'filter-click'}))
