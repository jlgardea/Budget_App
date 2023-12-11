from django.urls import path
from . import views

app_name = 'budgets'
urlpatterns = [
    path('', views.home, name='home'),
    path('budgets/<int:id>/', views.budgets, name='budgets'),
    path('transactions/<int:id>/', views.transactions, name='transactions'),
    path('account/<int:id>/', views.account, name='account'),
]