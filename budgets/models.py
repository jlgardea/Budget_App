from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    """An Account is a bank/credit card type of account"""
    CREDIT_CARD = "CC"
    BANK_ACCOUNT = "BA"
    ACCOUNT_TYPE_CHOICES = [
        (CREDIT_CARD, "Credit Card"),
        (BANK_ACCOUNT, "Bank Account"),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=25)
    balance = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    type = models.CharField(max_length=2, choices=ACCOUNT_TYPE_CHOICES, default=BANK_ACCOUNT)
    
class Budget(models.Model):
    CATEGORY_CHOICES = [
        ('Rent/Mortgage', 'Rent/Mortgage'),
        ('Transportation', 'Transportation'),
        ('Food', 'Food'),
        ('Healthcare', 'Healthcare'),
        ('Debt Repayment', 'Debt Repayment'),
        ('Savings', 'Savings'),
        ('Personal Care', 'Personal Care'),
        ('Entertainment', 'Entertainment'),
        ('Clothing', 'Clothing'),
        ('Utilities', 'Utilities'),
        ('Insurance', 'Insurance'),
        ('Childcare/Children Expenses', 'Childcare/Children Expenses'),
        ('Miscellaneous', 'Miscellaneous'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Miscellaneous')
    amount = models.DecimalField(max_digits=11, decimal_places=2)

class Transaction(models.Model):
    """A Transaction is a credit/debit from an account"""
    EXPENSE = 'EX'
    CREDIT = 'CR'
    #TRANSFER = 'TFR'
    TRANS_CHOICES = [
        (EXPENSE, 'Expense'),
        (CREDIT, 'Credit'),
        #(TRANSFER, 'Transfer'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=50)
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    type = models.CharField(max_length=3, choices=TRANS_CHOICES)
    category = models.CharField(max_length=50, choices=Budget.CATEGORY_CHOICES, blank=True, null=True)
    cleared = models.BooleanField(default=False)

    @property
    def owner(self):
        return self.account.owner
