"""Forms used in Checkout app."""

from django.contrib.auth.models import User
from django import forms
from .models import DeliveryDetail


class DeliveryDetailForm(forms.ModelForm):
    """Form for taking the delivery details."""

    # Textbox fields.
    name = forms.CharField(
        max_length=254, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True}))
    phone = forms.CharField(
        min_length=10, max_length=12, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True}))
    zip_code = forms.CharField(
        min_length=6, max_length=6, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True}))

    # Textarea fields.
    address = forms.CharField(
        max_length=254, required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': '3', 'required': True}))

    class Meta:
        """Meta for Delivery Detail."""

        # UserDetail model
        model = DeliveryDetail

        # Fields to exclude.
        exclude = ["user", "order_id", "quantity", "price",
                   "total", "product", "timestamp"]

    def clean_phone(self):
        """Custom validation of phone number field."""
        phone = self.cleaned_data.get('phone')
        try:
            int(phone)
        except (ValueError, TypeError):
            raise forms.ValidationError('Please enter a valid phone number')
        return phone

    def clean_zip_code(self):
        """Custom validation of zip code field."""
        zip_code = self.cleaned_data.get('zip_code')
        try:
            int(zip_code)
        except (ValueError, TypeError):
            raise forms.ValidationError('Please enter a zipcode')
        return zip_code


class DeliveryQuantityForm(forms.ModelForm):
    """Form for taking the updating quantity."""

    # NumberInput fields.
    quantity = forms.IntegerField(
        required=False, max_value=99, min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'value': '1', 'required': False}))

    class Meta:
        """Meta for Delivery Detail."""

        # UserDetail model
        model = DeliveryDetail

        # Fields to include.
        fields = ["quantity"]
