<img align="left" src="https://github.com/adamnapieralski/bd2-airport-parking-database/blob/master/airport_parking_site/parking_app/static/parking_app/favicon.png" title="ParkingApp" alt="ParkingApp" width="128" height="128">

# bd2-airport-parking-database

Project of the database of airport parking and web application for it's management and reporting. Made on Databases 2 course on FEIT of Warsaw University of Technology.

## Preview
![Start page](doc/images/app.png "Start page")
![Tickets](doc/images/tickets.png "Tickets")

| | | 
:-------------------------:|:-------------------------:
![](doc/images/my_reservations.png "My reservations")  |  ![](doc/images/add_reservation.png "Add reservation")
![Reporting_1](doc/images/reporting_1.png "Reporting - stats") | ![Reporting2](doc/images/reporting_2.png "Reporting - detailed preview")

## Installation
### Prerequisites
- python >= 3.6
- Django >= v3.0
- django-crispy-forms ([installation](https://django-crispy-forms.readthedocs.io/en/latest/install.html#installing-django-crispy-forms))

### Clone
Clone this repo to your local machine:
```
git clone https://github.com/adamnapieralski/bd2-airport-parking-database.git
```

### Setup
No specific setup apart from providing prerequisites is needed.

### Run
In `airport_parking_site` directory run django server:
```
python manage.py runserver
```
In your browser got to the displayed development server url (usually http://127.0.0.1:8000/).

## Tests
Run tests for whole application with:
```
python manage.py test
```
If more precise information about all executed tests is needed, set verbosity parameter:
```
python manage.py test -v 2
```
## Built With
- [Django](https://www.djangoproject.com/) - high-level Python Web framework that encourages rapid development and clean, pragmatic design
- [SQLite](https://www.sqlite.org/index.html) - a small, fast, self-contained, high-reliability, full-featured, SQL database engine

## Authors
- **Łukasz Kostrzewa** - [kost13](https://github.com/kost13)
- **Adam Napieralski** - [adamnapieralski](https://github.com/adamnapieralski)
- **Wojciech Wrzesień** - [wwrzesien](https://github.com/wwrzesien)
- **Marcin Gajewski** - [marcingajewski14](https://github.com/marcingajewski14)
