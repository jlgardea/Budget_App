from django.contrib import admin
from budgets.models import Account, Transaction, Budget

# Register your models here.
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Budget)

