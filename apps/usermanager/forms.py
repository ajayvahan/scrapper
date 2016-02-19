from django.contrib.auth.models import User
from django import forms
from .models import UserDetail


GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
)
MARITAL_CHOICES = (
    (1, 'Single'),
    (2, 'Married'),
)

class SignUpForm(forms.Form):

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    last_name = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False})
    )
    gender = forms.ChoiceField(
        required=False, choices=GENDER_CHOICES, widget=forms.RadioSelect())
    marital = forms.ChoiceField(required=False, choices=MARITAL_CHOICES)
    date_of_birth = forms.CharField(
        max_length=30, required=False,
        widget=forms.TextInput(attrs={
            'type': 'date', 'class': 'form-control'})
    )
    phone = forms.IntegerField(required=False)
    mail = forms.BooleanField(required=False)
    message = forms.BooleanField(required=False)
    phonecall = forms.BooleanField(required=False)
    other = forms.BooleanField(required=False)
    date_of_birth = forms.DateField(required=False, help_text='YYYY-MM-DD format')
    # address = forms.CharField(widget=forms.Textarea)


    class Meta:
        model = UserDetail
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'marital', 'phone',
                  'address', 'street', 'city', 'state', 'zip_code', 'mail',
                  'message', 'phonecall', 'other', 'extra_note', 'image']
        exclude = ["user"]

    def __init__(self, request, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # import pdb
        # pdb.set_trace()
        self.fields['first_name'].initial = request.user.first_name
        self.fields['last_name'].initial = request.user.last_name
        ud = UserDetail.objects.get(user=request.user)
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
