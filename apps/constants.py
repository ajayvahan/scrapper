"""Constants for home and usermanager apps."""

# Constants for setting
EMAIL_HOST = 'email.mindfiresolutions.com'
EMAIL_HOST_USER = 'ajay.vahan@mindfiresolutions.com'
EMAIL_HOST_PASSWORD = '1mfmail2016#'

# constants for usermanager app views
ACTIVATION_URL = "http://localhost:8000/activate/"

# constants for usermanager app models and forms
GENDER_CHOICES = (
    ('1', 'Male'),
    ('2', 'Female'),
)

MARITAL_CHOICES = (
    ('1', 'Single'),
    ('2', 'Married'),
)

# Constants for home app forms
SITE_CHOICES = (
    ('F', 'flipkart'),
    ('A', 'amazon')
)

# Constants for home app scrap
FLIPKART_URL = "http://www.flipkart.com"
AMAZON_URL = "http://www.amazon.in"
