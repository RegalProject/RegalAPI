# MyClosetAPI

## How to run Server
1. clone repository
2. cd to project folder
3. run:  
```ps
> pip install virtualenv
> virtualenv venv
> venv\Scripts\activate
> pip install -r requirements.txt
> python manage.py makemigrations core
> python manage.py makemigrations closet
> python manage.py migrate core
> python manage.py migrate closet
> python manage.py runserver
```
server will run on http://localhost:8000