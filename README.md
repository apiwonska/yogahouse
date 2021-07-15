# Yoga House App

Live demo: [url](urlname)

A website for fake yoga school with class schedule, blog, contact form and admin panel. App fully created with Django framework.
This was the first Django project ever that I have created, so don't expect too much in terms of good quality code ;-)

You can log in to admin panel as user1 with view permissions for all models.
login: user1, password: P@ssword123

## Main features:

* Home page and page with class descriptions
* Class schedule, where students can sign up for lessons
* Blog
* Contact form
* Admin panel for managing app content especially usefull for controlling class schedule

## Used technologies and libraries:

* Django framework
* Bootstrap

## Setup for developement:

Prerequisites: you need to install python3, python3-pip, python3-venv  on your machine.

* Clone the repository
```
git clone https://github.com/apiwonska/yogahouse.git
```
* Setup and activate the virtual envirnonment on your computer (anywhere outside the project)
```
$ python3 -m venv myvenv
$ . myvenv/bin/activate
```
* Move to the project directory and install project dependencies.
```
$ pip install requirements.txt
```
* Setup a Postgres DB, create user & database
* Create a file .env in project root directory next to manage.py
* Write following environment variables in your .env file
```
SECRET_KEY=your_django_app_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_db_user_name
DB_PORT=your_db_port
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
EMAIL_HOST=your_email_host
EMAIL_HOST_USER=your_email_host_user
EMAIL_HOST_PASSWORD=your_email_host_password
EMAIL_PORT=your_email_port
```
* Make migrations
```
$ python manage.py migrate
```
* Create admin account
```
$ python manage.py createsuperuser
```
* Make migrations
```
$ python manage.py makemigrations yogahouse
$ python manage.py migrate
```
* Start the developement server
```
$ python manage.py runserver
```
* Open localhost:8000 in the browser to see the app.
* Url for admin panel http://localhost:8000/admin/ 


## Credits:

* Icons come from: fontawsome.com
* Photos come from unsplash.com

## To improve:

* Improve accessibility
* Conform to the PEP 8 style guide