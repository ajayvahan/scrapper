Scrapper
====================================================================
Overview:
--------------------------------------------------------------------
Web Scraping (also termed Screen Scraping, Web Data Extraction, Web Harvesting etc) is a technique employed to extract large amounts of data from websites whereby the data is extracted and saved to a local file in your computer or to a database in table (spreadsheet) format. 

This application allow user to scrap the products details from flipkart and amazon based on search argument. Extracted data is save to the database, from thier we use it to display that items in our application.


Requirements:
--------------------------------------------------------------------

	Python 3.4.3
	MySQL client 1.3.7
	MechanicalSoup 0.4.0
	Pillow 3.1.1
	decorator 4.0.6
	virtualenv
	Django 1.8
	beautifulsoup4 4.4.1
	ipython 4.0.3
	ipython-genutils 0.1.0
	path.py 8.1.2
	pexpect 4.0.1
	pickleshare 0.6
	ptyprocess 0.5
	pytz 2015.7
	requests 2.9.1
	simplegeneric 0.8.1
	six 1.10.0
	traitlets 4.1.0
	wheel 0.24.0


Technologies Used:
---------------------------------------------------------------------

Backend:
	Django 1.8
	MySQL 1.3.7

Front end:
	HTML5
	CSS3
	Bootstrap 3
	jQuery

Installation:
----------------------------------------------------------------------

Before you start scraping, you will have to set up a new Scrapper project.

Step 1: Create a separate virtual environment with python 3.4 for our project.
		
		$ pip install virtualenv
		$ virtualenv -p /usr/bin/python3 env/py34
		$ source env/py34/bin/activate

Step 2: In the environment install django and all other required pakages mentioned above.

Step 3: Clone the project to your folder. Enter a directory where you’d like to store the project and run:
		$ git clone https://github.com/ajayvahan/scrapper.git


Step 4: Create a empty database named "scrapper".

Step 5: Confuger your database and email in settinds.py

		DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'scrapper',
	        'USER': 'mysql client username',
	        'PASSWORD': 'mysql client password',
	        'HOST': '',
	        'PORT': '',
	    	}
		}

		EMAIL_HOST = 'your email host'
		EMAIL_HOST_USER = 'email username'
		EMAIL_HOST_PASSWORD = 'email password'
		EMAIL_PORT = 587
		EMAIL_USE_TLS = True


Step 6: Enter the scrapper directory and run the following command to create tables for the project.
		$ python manage.py makemigrations
		$ python manage.py migrate

Step 7: Run server
		$ python manage.py runserver

Step 8: In browser url run  http://localhost:8000
