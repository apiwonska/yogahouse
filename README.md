# Yoga House App

Live demo: [https://yogahouse-ap.herokuapp.com](YogaHouse)

A website for fake yoga school with class schedule, blog, contact form and admin panel. App fully created with Django framework. The project was created to learn the basics of Django framework.

This was the first bigger project. It is written with little use of js which I didn't know at the point of creating this app.
With time tests were added and main accessibility issues fixed.

You can log in to the admin panel as user1 with view permissions for all models.
login: user1, password: P@ssword123

## Main features:
* Admin panel for managing application content
* User can create an account and recuperate the password if lost. 
* Home page - not editable with the admin site
* About page - admin can add and modify instructors data
* Prices page - admin can add and modify information about prices.
* Classes page - admin can add and modify class types
* Terms and conditions page - admin can add and modify content
* **Schedule** page - responsive schedule in form of a table for large screens and accordion for small screens.
An authenticated user can sign for a scheduled class or sign off if necessary. For the table schedule, the modal displays the number of available places as well as information about class and teacher. Table schedule can also be searched by class type. The accordion schedule lack this functionality. It is only possible to sign up or off the class.
Users can view scheduled classes for the coming weeks. It's not possible to sign up for the class in the past.
Users can view and search a list of classes for which they signed up.
Site admin can add new types of classes, new courses and schedule classes. 
* Blog and event pages. Site admin can create and modify items.
* Contact form

## Used technologies and libraries:
* Django framework
* Bootstrap
* django-imagekit
* django-ckeditor
* Postgresql

## Setup for developement:
Prerequisites: you need to install python3, python3-pip, python3-venv  on your machine.

* Clone the repository
```
git clone https://github.com/apiwonska/yogahouse.git
```
* Setup and activate the virtual environment on your computer (anywhere outside the project)
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
* Create an admin account
```
$ python manage.py createsuperuser
```
* Make migrations
```
$ python manage.py makemigrations
$ python manage.py migrate
```
* Start the development server
```
$ python manage.py runserver
```
* Open localhost:8000 in the browser to see the app.
* Url for admin panel http://localhost:8000/admin/ 

## Credits:
* Icons come from: fontawsome.com
* Photos come from unsplash.com

## To improve:
* Rewrite schedule application with the use of js and endpoints to read and write data to the database.
* Conform to the PEP 8 style guide