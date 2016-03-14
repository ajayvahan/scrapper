"""Forms for usermanager.

It contains registeration form for signup page, login form
for login page and edit form for edit profile page.
"""

from django import forms
from .models import UserDetail
from apps import constants as con


class SignUpForm(forms.Form):
    """Registeration form for signup page.

    It provide all the fields needed for registeration form.
    """

    # Textbox fields.
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'required': False, 'autofocus': True,
                'placeholder': 'First name'}))
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'required': False, 'autofocus': True,
                'placeholder': 'Last name'}))
    username = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'required': False, 'autofocus': True,
                'placeholder': 'Username'}))

    # Email field.
    email = forms.EmailField(
        max_length=254, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'required': False, 'autofocus': True,
                'placeholder': 'Email'}))

    # Password fields.
    password = forms.CharField(
        max_length=128, required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'required': False, 'autofocus': True,
                'placeholder': 'Password'}))
    confirm_password = forms.CharField(
        max_length=128, required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'required': False, 'autofocus': True,
                'placeholder': 'Confirm password'}))


class LoginForm(forms.Form):
    """Login form for login page.

    It provide all the fields needed for login form.
    """

    # Textbox fields.
    username = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'required': False, 'autofocus': True,
                'placeholder': 'Username'}))

    # Password field.
    password = forms.CharField(
        max_length=128, required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'required': False, 'autofocus': True,
                'placeholder': 'Password'}))


class EditProfileForm(forms.ModelForm):
    """Edit profile form.

    It provide all the fields needed for edit profile form.
    """

    # Textbox fields.
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))

    # Radio field.
    gender = forms.ChoiceField(
        choices=con.GENDER_CHOICES, required=False,
        widget=forms.RadioSelect(attrs={'required': False}))

    # Date field.
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'date', 'class': 'form-control'}))

    # Dropdown field.
    marital = forms.ChoiceField(
        choices=con.MARITAL_CHOICES, required=False)

    # Number field.
    phone = forms.CharField(
        max_length=12, min_length=10, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))

    # Textarea field.
    address = forms.CharField(
        max_length=150, required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 3}))

    # Textbox fields.
    street = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    city = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    state = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    zip_code = forms.CharField(
        max_length=6, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))

    # Checkbox fields.
    mail = forms.BooleanField(required=False)
    message = forms.BooleanField(required=False)
    phonecall = forms.BooleanField(required=False)
    other = forms.BooleanField(required=False)
    extra_note = forms.CharField(
        required=False, widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 3}))

    # Image field.
    image = forms.ImageField(required=False)

    class Meta:
        """Meta for UserDetail."""

        # UserDetail model
        model = UserDetail

        # Fields to include.
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth',
                  'marital', 'phone', 'address', 'street', 'city',
                  'state', 'zip_code', 'mail', 'message', 'phonecall',
                  'other', 'extra_note', 'image']

        # Fields to exclude.
        exclude = ["user"]

    def clean_phone(self):
        """Custom validation of phone number field."""
        phone = self.cleaned_data.get('phone')
        try:
            int(phone)
        except (ValueError, TypeError):
            raise forms.ValidationError('Please enter a valid phone number')
        return phone

    def __init__(self, request, *args, **kwargs):
        """Setting initial value for fields."""
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Feilds from auth_user table.
        self.fields['first_name'].initial = request.user.first_name
        self.fields['last_name'].initial = request.user.last_name

        # Creating UserDetail reference where user_id
        ud = UserDetail.objects.get(user=request.user)

        # Feilds from UserDetail.
        self.fields['city'].initial = ud.city
        self.fields['gender'].initial = ud.gender
        self.fields['date_of_birth'].initial = ud.date_of_birth
        self.fields['marital'].initial = ud.marital
        self.fields['phone'].initial = ud.phone
        self.fields['address'].initial = ud.address
        self.fields['street'].initial = ud.street
        self.fields['zip_code'].initial = ud.zip_code
        self.fields['state'].initial = ud.state
        self.fields['mail'].initial = ud.mail
        self.fields['message'].initial = ud.message
        self.fields['phonecall'].initial = ud.phonecall
        self.fields['other'].initial = ud.other
        self.fields['extra_note'].initial = ud.extra_note
