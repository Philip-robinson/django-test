from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('api/shares', views.apishares, name='apishares'),
    path('api/transactions/<int:id>',
        views.api_transactions, name='api_transactions'),
    path('api/prices/<int:id>',
        views.api_price_changes, name='api_price_changes'),
]

