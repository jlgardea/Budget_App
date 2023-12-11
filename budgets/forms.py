from django import forms
from django.forms import ModelForm
from . models import Account, Budget, Transaction

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ["nickname", "type"]

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["transaction_date", "account", "type", "text", "amount", "category"]

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'category']
