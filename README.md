# Event management
> Using this project you can view all events and register using email to add your own events with info and timestamp.

## Installing

Python3 must be already installed

```shell
git clone https://github.com/LiudmylaKulinchenko/event-management.git  # clone project to your PK
cd event-management/  # change directory to the project directory
python -m venv venv
venv/Scripts/activate  # create and activate virtual environment
pip install -r requirements.txt  # install requirements
python manage.py makemigrations
python manage.py migrate  # create database
python manage.py runserver  # starts Django Server
```

## Features

What's all the bells and whistles this project can perform?
* Listing all events for not authenticated users
* Authentication fuctionality for User using email! You don't have to remember your freak username here, so be creative!
* Adding new events and event types (you also can create event with not excisting event type - it will be added automaticaly!)
* Admin panel for advanced managing, where you can filter events by event type and timestamp

## Links

- Project events page: http://127.0.0.1:8000/api/event/events/
- Repository: https://github.com/LiudmylaKulinchenko/event-management.git
