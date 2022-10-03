# Creating a website with pyton and django.

I have had some success creating django projects using the command line.

PyCharm seems to work but only the paid for version properly
supports Django even the paid for InteliJ does not well support Django.

The following however is mostly command line stuff and was mostly
taken from
https://www.w3schools.com/django/django\_create\_project.php

What seems to be important about django is the directory structure.

## setup the project
First create the project, you need to have installed python and django,
how you do this depends on your os so will not ve described here.

On the system used for this work the installed software was:

* python 3.10
* django 4.1
* ubuntu 22.04


Go to the directory into which you want to place the project
then, on the command line run

```
$ django-admin startproject projectNumber1

```
This creates a subdirectory called __projectNumber1__ containing the
file manage.py which is used to perform management tasks within the 
project.

It also contains a subdirectory with the same name __projectNumber1__
which is the project proper.

```
projectNumber1
    |
    +--- manage.py
    +--- projectNumber1
             |
             +--- urls.py
             +--- __init__.py
             +--- wsgi.py
             +--- asgi.py
             +--- settings.py

```

if you now step into the directory that contains manage.py you can run

```
$ python manage.py runserver
```

This will start up a web server, no content added yet, but a default
page is displayedi, by default this can be found at:

http://localhost:8000

This server is net meant for production but is great for testing.

NOTiE: This next bit I am a bit foggy about as it is new to me,
but I currently think the following is true:

In the world of Django a project contains a series of apps, each
being a small part of the whole, perhaps an individual page or
database connection.

## Database

Django is not meant to work without a database. by default it will
use an inbuilt sqlite which can be configured for in memory or for
it's data to be stored in the file system.

Even if you have no use for the database Django still expects it to be.

If not configured otherwise an sqlite database will be created when
an app is first created, so we are now going to create the first app
and configure the database:

### Create the first app

Create the app home:

Using the command line from the directory containing manage.py

```
$ python manage.py startapp home
```

This will create a new directory __home__ containing teh following files:

```
home
   |
   +--- migrations
   +--- migrations/__init__.py
   +--- tests.py
   +--- __init__.py
   +--- admin.py
   +--- models.py
   +--- apps.py
   +--- views.py
```

It will also add a file db.sqlite3 which is an sqlite database
file to te root directory and a cache directory __ \_\_pycache\_\_ __ to
the project directory, that is under __projectNumber1__.

### Database configuration

We are going to have a database containing share information, the
following tables will be needed:

* Shares
	* name, 256 char text field.
* Transactions
	* share, reference to Share
	* date, date of transaction
	* buy\_sell, enumeration SELL or BUY.
	* number, number of shares
	* cost, number, total amount paid or receieved.
* Price\_changes
	* share, reference to Share
	*  date, date of transaction
	*  price, number

First we need to register the app:

Edit __projectNumber1/settings.py__ adding the __home.apps.HomeConfig__
to the app list

Take the list __INSTALLED_APPS__ and add a line to the end so it becomes:

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home.apps.HomeConfig',
]

```
 
We can now edit home/models.py to configure the database.

```
from django.db import models

# Create your models here.

class Shares(models.Model):
    name = models.CharField(max_length=255)


class Transactions(models.Model):
    BUY_SELL = (('BUY', 'Buy'),('SELL', 'Sell'))
    share = models.ForeignKey(Shares, on_delete=models.CASCADE)
    date = models.DateField()
    buy_sell = models.CharField(max_length=4, choices=BUY_SELL)
    number = models.IntegerField()
    cost = models.DecimalField(max_digits=12, decimal_places=4)


class Price_Changes(models.Model):
    share = models.ForeignKey(Shares, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=4)


```

To add these tables to the sqlite database go into the directory were
the __manage.py__ script resides and execute:

```
$ python manage.py makemigrations home
$ python manage.py migrate
```

The first of these creates a script specifying the database changes
that msut be made and the second applies them to the database.

If we fire up the shell we can manually populate and view the database
using the type of python that will be used when writing the code:

```
from home.models import Shares, Transactions, Price_Changes
Shares.objects.all()
```

Will list all known shares which are currently none, but shares can be
added.

you will always need
```
from home.models import Shares, Transactions, Price_Changes
```

At thr e top of the file, but as this has been dne provided you have
not exited the shell we will not need to repeat it.

```
share = Shares(name='Share number one')
share.save()
```
or more concisely
```
Shares(name='Share number two').save()
```

We can also add a price change for both shares, if you execute
__Shares.objectd.all().values()__ you can see iall the fields of
the shares we have created including their id.

```
Shares.objects.all().values()
<QuerySet [
		{'id': 1, 'name': 'Share number one'},
		{'id': 2, 'name': 'Share number two'}
]>

Price_Changes(share_id=1, date=datetime.datetime.now(), price=23.34).save()
Price_Changes(share_id=2, date=datetime.datetime.now(), price=1323.50).save()

Price_Changes.objects.all().values()
<QuerySet [
		{'id': 1,
		 'share_id': 1,
     'date': datetime.date(2022, 10, 2),
     'price': Decimal('23.3400')},
		{'id': 2,
     'share_id': 2,
     'date': datetime.date(2022, 10, 2),
     'price': Decimal('1323.5000')}
]>

```

if we now add another date change:

```
Price_Changes(share_id=2, date=datetime.datetime.now(), price=1000).save()
```

we can now do some queries __Q__ is helpful with generating queries,
the double underscore __ \_\_ __ has a special meaning iand relates to 
functions that have been autogenerated by Django to aid with the
execution of queries.

```
from django.db.models import Q
x = Price_Changes.objects.filter(Q(share__name__contains='two'))
```

The query section __share__name__contains='two'__ 
means the foreign key shire matches a Shire with a name 
entry that contains the word two, this will 
result in x being a list of the two price changes:

```
print(x)
<QuerySet [
    <Price_Changes: Price_Changes object (2)>,
    <Price_Changes: Price_Changes object (3)>
]>
```
