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
page is displayed, by default this can be found at:

http://localhost:8000

This server is not meant for production but is great for testing.

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
file to the root directory and a cache directory __ \_\_pycache\_\_ __ to
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
that must be made and the second applies them to the database.

If we fire up the shell we can manually populate and view the database
using the type of python that will be used when writing the code:

```
from home.models import Shares, Transactions, Price_Changes
Shares.objects.all()
```

Will list all known shares which are currently none, but shares can be
added.

```
from home.models import Shares, Transactions, Price_Changes
share = Shares(name='Share number one')
share.save()
```
or more concisely
```
Shares(name='Share number two').save()
```

We can also add a price change for both shares, if you execute
__Shares.objectd.all().values()__ you can see all the fields of
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

```
x = Price_Changes.objects.filter(share__name__contains='two')
```

The query section __share__name__contains='two'__ 
means the foreign key shire matches a Shire with a name 
entry that contains the word two, this will 
result in x being a list of the two price changes (Note that the syntax
of the queries is described on the internet):

```
print(x)
<QuerySet [
    <Price_Changes: Price_Changes object (2)>,
    <Price_Changes: Price_Changes object (3)>
]>
```

# A view of the data

To create a view of the data first add a template file at __home/templates/home.html__ and put some html.

```
<html>
    <head>
        <title>{{title}}</title>
    </head>
    <body>
        <h1>Shares</h1>

        <table>
        {% for x in companies %}
            <tr>
                <td>{{ x.name }}</td>
                <td><a href="/shares/detail/{{ x.id }}">detail</a></td>
            </tr>
        {% endfor %}
        </table>
    </body>
</html>
```

modify the file __home/views.js__ to be:
```
from django.http import HttpResponse
from django.template import loader
from .models import Shares, Transactions, Price_Changes

def index(request):
  template = loader.get_template('home.html')
  context = {
    'companies': Shares.objects.all().values(),
  }
  return HttpResponse(template.render(context, request))
```

Run the server:
```
python manage.py runserver
```
and pint your browser at __http://localhost:8000/shares__

/shares because that is specified in the __projectNumber1/urls.py__

The displayed page shows the share names we have in the database and for each one a link to show more details.

The show detail url now needs to be implemented.

Create a new template __home/templates/detail.html__
```
<html>
    <head>
        <title>{{title}}</title>
    </head>
    <body>
        <h1>Details of {{name}}</h1>

	<h2>Transactions</ht>
        <table>
            <tr><th>Date</th><th>buy or sell</th>
                <th>Number</th><th>Total cost</th></tr>
        {% for x in transactions %}
            <tr>
                <td>{{ x.date }}</td>
                <td>{{ x.buy_sell }}</td>
                <td>{{ x.number }}</td>
                <td>{{ x.cost }}</td>
            </tr>
        {% endfor %}
        </table>
	<h2>Price changes</ht>
        <table>
            <tr><th>Date</th><th>New price</th></tr>
        {% for x in prices %}
            <tr>
                <td>{{ x.date }}</td>
                <td>{{ x.price }}</td>
            </tr>
        {% endfor %}
        </table>
    </body>
</html>

```

add a function to __home/views.py__
```
def detail(request, id):
    template = loader.get_template("detail.html")
    name = Shares.objects.get(id=id).name
    context = {
        "title": r"Deatils of {name}",
        "name": name,
        "transactions": Transactions.objects.filter(share__id=id),
        "prices": Price_Changes.objects.filter(share__id=id),
    }
    return HttpResponse(template.render(context, request))

```

Add a new entry to ithe __urlpatters__ list in __home/urls.py__
```
path('detail/<int:id>', views.detail, name='detail'),
```
The section /<int:id> means that a variable is epected at the end of the url
which will be call id and is an integer

If the server has been running all this time it should automatically restart
if not then start it again

using the browser pointing at __http://localhost:8000/shares__

you should see something like:
```
Shares
Share number one 	detail
Share number two 	detail
```

clicking on the detail link should take us to __http://localhost:8000/shares/detail/1__
or __http://localhost:8000/shares/detail/2__ depending on which one is clicked, these
should open the newly created details page and display something like```
Details of Share number two
Transactions
Date	buy or sell 	Number	Total cost
Price changes
Date	New price
Oct. 2, 2022 	1323.5000
Oct. 2, 2022 	1000.0000
```

No transactions are shown because we never entered anything into the transactions table
the price changes are taken from the Price_Change table.

## Adding css

This is amazingly hard, I would go to flask for this alone.

There are two mechanisms for delivering static files, one
works in dev and the other in production, this is because for production 
purposes the built in web server is not used they assume that the
static files are delivered by some external web server.

we can add a static css file at __home/static/home/style.css__

First add a request for the stylesheet into the headers of both templates.
```
<link rel="stylesheet" href="/static/home/style.css" />

```

Then create the stylesheet in a directory called static under your app.

__home/static/home/style.css__

```
html {
 font-family: sans-serif;s
 background: #eee;
 padding: 5px;
}
body {
 max-width: 1200px;
 margin: 0 auto;
 background: white;
}
h1 {
 font-family: serif;
 color: #377ba8;
 margin: 5px 20px;
}
table{
  border: 1px solid blue;
  padding: 5px;
  margin: 5px;
}
table tr:nth-child(2n+1) td{
  background-color: #fed;
}

```

You should then have a perttier display.

## Provideing Restful API data

We can add the following three urlpatterns to __home/urls.py__

```
     path('api/shares', views.apishares, name='apishares'),
     path('api/transactions/<int:id>',
         views.api_transactions, name='api_transactions'),
     path('api/prices/<int:id>',
         views.api_price_changes, name='api_price_changes'),
 
```

and the following three functions to __home/views.py__

```

def apishares(request):
    return JsonResponse({"shares":
        [v for v in Shares.objects.all().values()]})

def api_price_changes(request, id):
    return JsonResponse({"prices":
        [v for v in Price_Changes.objects.filter(share__id=id).values()]})

def api_transactions(request, id):
    return JsonResponse({"transactions":
        [v for v in Transactions.objects.filter(share__id=id).values()]})

```

The odd thing about this code really is that the JsonParser is very fussy
about what it will process and will not preocess the results of a database
query directly, so these query results need to be convered to simple lists
dictionaries.

These view can now be accessed at
* __http://localhost:8000/shares/api/shares__
* __http://localhost:8000/shares/api/prices/id_ where id should be replaced
by the id of the relevant share.
* __http://localhost:8000/shares/api/transactions/id_ where id should be replaced
by the id of the relevant share.



