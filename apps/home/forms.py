from django import forms


SITE_CHOICES = (
    ('F', 'flipkart'),
    ('A', 'amazon')
)


class ScrapSearchForm(forms.Form):
    """Search form for scraping."""

    search_item = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required':True}))
    site_choice = forms.ChoiceField(
        required=False, choices=SITE_CHOICES, widget=forms.RadioSelect(attrs={'required':True}))


class DashboardSearchForm(forms.Form):
    """Search products from database."""

    search_item = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required':True}))
