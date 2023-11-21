# Project Info
This project is related to the <a href='https://sabzlearn.ir/'>Sabzlearn</a> course and I did this project after seeing that period.
During that course, 2 projects were done and this project is the first project that I did.

## Environment Setup 🚀


git clone https://github.com/MahdiMalvandi/my-first-django-project.git
```

```terminal
cd my-first-django-project/
```

If virtualenv is not installed [(What is virtualenv?)](https://www.youtube.com/watch?v=N5vscPTWKOk&t=313s):

```terminal 
pip install virtualenv
```

Create a virtual environment

```terminal 
virtualenv venv
```

Activate the environment everytime you open the project

`$ source venv/Scripts/activate`

Install requirements 🛠

`$ pip install -r requirements.txt`

`$ pre-commit install`

Run migrations for Database


```terminal python manage.py migrate```

Create superuser for Admin Login 🔐

`$ python manage.py createsuperuser`

Enter your desired username, email and password. Make sure you remember them as you'll need them in future.

eg.

    Username: admin

    Email: admin@admin.com

    Password: HighlyConfidentialPassword

All Set! 🤩

Now you can run the server to see your application up & running 🚀

`$ python manage.py runserver`

To exit the environment ❎

`$ deactivate`

Every time you want to open the application in browser, make sure you run:

`$ source venv/Scripts/activate`

`$ python manage.py runserver`


Then the database should be migrated with this command:
```terminal
python
```
