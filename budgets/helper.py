from django.db.models import Sum
from datetime import date
from . models import Account, Budget, Transaction
from . forms import AccountForm, BudgetForm, TransactionForm

def add_account(form, user):
    new_account = form.save(commit=False)
    new_account.owner = user
    new_account.balance = 0.00
    new_account.save()
    print("Account Saved")

def update_balance(transaction):
    transaction_type = transaction.type
    account = transaction.account

    if transaction_type == 'EX':
        account.balance -= transaction.amount
    elif transaction_type == 'CR':
        account.balance += transaction.amount

    account.save()
    print('Balance Updated')

def delete_transaction(transaction_id):
    delete_transaction = Transaction.objects.get(id=transaction_id)
    delete_transaction.amount *= -1
    update_balance(delete_transaction)
    delete_transaction.delete()
    print('Transaction Deleted')

def add_budget(form, user):
    new_budget = form.save(commit=False)
    new_budget.owner = user
    new_budget.save()
    print("Budget Saved")

def delete_budget(budget_id):
    delete_budget = Budget.objects.get(id=budget_id)
    delete_budget.delete()
    print('Budget Deleted')

def get_budget_mtd_information(user_categories, user_id):
    today = date.today()
    budget_mtd_list = {}

    for item in user_categories:

        item_details = {}
        #find all users transactions for budget category
        associated_transactions = Transaction.objects.filter(
            account__owner=user_id,
            transaction_date__month=today.month, 
            transaction_date__year=today.year,
            category=item.category
        )

        #calculate the month to date total for transactions
        month_to_date_total = associated_transactions.aggregate(
            Sum('amount', default=0.00)
        )
        mtd = month_to_date_total['amount__sum']
        item_details['mtd'] = round(mtd, 2)

        #find the difference between month spent and allocated budget amount
        balance_left_over =  item.amount - mtd
        item_details['balance'] = round(balance_left_over, 2)

        #get the percentage of money spent vs budget amount
        progress_percentage = mtd / item.amount * 100
        item_details['progress'] = int(progress_percentage)

        budget_mtd_list[item] =  item_details

    return budget_mtd_list
