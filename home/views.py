from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from .models import Shares, Transactions, Price_Changes
from json import dumps

def index(request):
    template = loader.get_template('home.html')
    context = {
        "title": "Companies",
        'companies': Shares.objects.all().values(),
    } 
    return HttpResponse(template.render(context, request))

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

def apishares(request):
    # This silly shenanagins is because the json serialiser
    # will not serialise query results
    return JsonResponse({"shares":
        [v for v in Shares.objects.all().values()]})

def api_price_changes(request, id):
    return JsonResponse({"prices":
        [v for v in Price_Changes.objects.filter(share__id=id).values()]})

def api_transactions(request, id):
    return JsonResponse({"transactions":
        [v for v in Transactions.objects.filter(share__id=id).values()]})

