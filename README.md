# Taxi Service Project

Django project for managing drivers and cars in Taxi

## Check it out

[Taxi service project deployed to Heroku](https://taxi-service-web-app.herokuapp.com/)

## Installation

Python3 must be already installed
```shell
git clone https://github.com/liuda-chuzdiuk/taxi-service.git
python3 -m venv venv
source venv/bin/activate (on macOS) & venv\Scripts\activate (on Windows)
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py runserver # starts Django Server
```

## Features
* Authentication functionality for Driver/User
* Managing cars, manufacturers, drivers directly from website interface
* Powerful admin panel for advanced managing

## Demo

![Website interface](demo.png)
