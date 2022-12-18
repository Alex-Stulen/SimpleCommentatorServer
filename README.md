
# Simple Commentator | Server Side

---

### Description:

The back end of the [Simple Commentator](https://simple-commentator.com) project.

Project for simple commenting. Ability to leave comments, reply to comments, attach a file, edit comment text as html, etc.

---

### Pre-requirements:

* Python 3.6+ (developed and tested on version 3.10.8). Recommended Version: 3.10.8
* PostgreSQL (developed and tested on version 14.5). Recommended Version: 14.5
* Having an .env file at the root of the project (See section .ENV Description)

---

### Technologies:

* Python
* Django
* Django REST Framework
* PostgreSQL
* Gunicorn
* Nginx
* Git

### Requirements:

All project dependencies in the **requirements.txt** file in the project root folder

---

### .ENV Description:

Description of all fields in the .env file

File format: Pairs <-key->=<-value->. Be sure to write equal between key and value without spaces
Pairs are separated by \n (each pair on a new line) 

**SECRET_KEY**=<string: django secret key>

**DEBUG**=<bool: True or False>

**ALLOWED_HOSTS_SEPARATOR**=<string: allowed host separator. Ex: ;>

**ALLOWED_HOSTS**=<string: allowed hosts separated by ALLOWED_HOSTS SEPARATOR. Ex: 127.0.0.1;localhost;192.168.31.201>

**DATABASE_NAME**=<string: database name>

**DATABASE_USER**=<string: database user username>

**DATABASE_PASSWORD**=<string: database user password>

**DATABASE_HOST**=<string: database host>

**DATABASE_PORT**=<int: database port>

**LANGUAGE_CODE**=<string: language code. Ex: en-us>

**TIME_ZONE**=<string: time zone name>

**USE_I18N**=<bool: True or False>

**USE_TZ**=<bool: True or False>

**RECAPTCH_SITE_KEY**=<string: public captcha token>

**RECAPTCH_SECRET_KEY**=<string: private captcha token>

**CORS_ALLOWED_ORIGINS_SEPARATOR**=<string: separator for CORS_ALLOWED_ORIGINS. Ex: ;>

**CORS_ALLOWED_ORIGINS**=<string: allowed cors hosts separated by CORS_ALLOWED_ORIGINS SEPARATOR. Ex: http://localhost:8080;http://192.168.31.201:8080>

---

### .env file example:

See the **.env.example** file at the root of the project

---

### Project startup:

1. Clone project from github

    <code>git clone git@github.com:Alex-Stulen/SimpleCommentatorServer.git</code>
2. Create an empty python virtual environment

    <code>python -m venv venv</code> or through the **virtualenv** utility
3. Install dependencies from requirements.txt file

   <code>pip install -r requirements.txt</code> 
4. Create a database (postgresql) and a user for the database
5. Create and configure an .env file at the root of the project at the level of the manage.py file
6. Run the migrations

    <code>python manage.py migrate</code>
7. Run a collection of statics

    <code>python manage.py collectstatic</code>
8. Create a superuser

    <code>python manage.py createsuperuser</code>
9. Start the server

    <code>python manage.py runserver</code>

---

## Author
Alex Stulen

Email: **ookno16@gmail.com**

Telegram: **@stule_o**

Developed and written in December 2022
