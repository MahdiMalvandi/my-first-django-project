# Project Info
This project is related to the <a href='https://sabzlearn.ir/'>Sabzlearn</a> course and I did this project after seeing that period.
During that course, 2 projects were done and this project is the first project that I did.

## Environment Setup 🚀

```terminal
git clone https://github.com/MahdiMalvandi/my-first-django-project.git
```
Enter the project folder

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

```terminal 
source venv/Scripts/activate
```

Install requirements 🛠

```terminal 
pip install -r requirements.txt
```

Run migrations for Database


```terminal 
python manage.py migrate
```

Create superuser for Admin Login 🔐


```terminal 
python manage.py createsuperuser
```

Now you can run the server to see your application up & running 🚀

```terminal
python manage.py runserver
```
