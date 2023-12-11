from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Sum, FloatField
from datetime import date
from . models import Account, Budget, Transaction
from . forms import AccountForm, BudgetForm, TransactionForm
from . helper import *

# Create your views here.
@login_required
def home(request):
    """"
    Home Page for Budget App:
    View Accounts, View Budget Snapshot, Create New Account
    """
    context = {}
    print(request.POST)

    if request.method == "POST":
        #Create a new account with NewAcct submission and redirect to home page
        if 'NewAcct' in request.POST:
            form = AccountForm(data=request.POST)
            if form.is_valid():
                add_account(form, request.user)
                return redirect('/')

    #Get information for navbar
    accounts = Account.objects.filter(owner=request.user).order_by('nickname')
    context['accounts'] = accounts

    #Get information for displaying current accounts
    context['bank_accts'] = accounts.filter(type='BA').order_by('nickname')
    context['credit_accts'] = accounts.filter(type='CC').order_by('nickname')
    context['types'] = sorted(Account.ACCOUNT_TYPE_CHOICES)

    #Get information for displaying budget snapshot
    user_budgets = Budget.objects.filter(owner=request.user.id).order_by('category')
    sum_of_user_budgets =  get_budget_mtd_information(user_budgets, request.user)
    context['sum_of_user_budgets'] = sum_of_user_budgets
    
    return render(request, 'budgets/home.html', context)


@login_required
def account(request, id):
    """
    Account ID's Page: 
    Delete Account, Add New Transaction, Delete Transaction
    """
    account = get_object_or_404(Account, id=id)
    context = {}
    print(request.POST)

    #Verify the account belongs to authenticated user
    if account.owner != request.user:
        raise Http404

    if request.method == "POST":
        #Delete Account and redirect to home page
        if 'DelAcct' in request.POST:
            account.delete()
            return redirect('/')

        #Create a new transaction with NewTrans submission and return to account page
        elif 'NewTrans' in request.POST:
            form = TransactionForm(data=request.POST)
            if form.is_valid():
                new_transaction = form.save(commit=False)
                update_balance(new_transaction)
                new_transaction.save()
            return HttpResponseRedirect('/account/'+ str(id))

        #Delete selected transaction with DelTrans submission and return to account page
        elif 'DelTrans' in request.POST:
            transaction_pk = request.POST.get('DelTrans')
            delete_transaction(transaction_pk)
            return HttpResponseRedirect('/account/'+ str(id))


    #Get information for navbar and form submission
    context["accounts"] = Account.objects.filter(owner=request.user).order_by('nickname')

    #Get information for transaction list
    transactions = Transaction.objects.filter(account=id).order_by('-transaction_date', '-date_added')
    context["categories"] = sorted(Budget.CATEGORY_CHOICES)
    context["type_list"] = sorted(Transaction.TRANS_CHOICES)
    context["account"] = account
    context['transactions'] = transactions

    #paginator
    paginator = Paginator(transactions, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj

    return render(request, 'budgets/account.html', context)


@login_required
def transactions(request, id):
    """
    User Transaction Page: 
    Add New Transaction, Delete Transaction
    """
    context = {}
    print(request.POST)
    
    #Verify the transaction page belongs to authenticated user
    if id != request.user.id:
        raise Http404

    if request.method == "POST":
        #Create a new transaction with NewTrans submission and return to transaction page
        if 'NewTrans' in request.POST:
            form = TransactionForm(data=request.POST)
            if form.is_valid():
                new_transaction = form.save(commit=False)
                update_balance(new_transaction)
                new_transaction.save()

        #Delete selected transaction with DelTrans submission and return to transaction page       
        elif 'DelTrans' in request.POST:
            transaction_pk = request.POST.get('DelTrans')
            delete_transaction(transaction_pk)
    
    #find all transactions linked to user
    accounts = Account.objects.filter(owner=id).order_by('nickname')
    user_transactions = Transaction.objects.filter(account__owner=id).order_by('-transaction_date', '-date_added')
    context["transactions"] = user_transactions

    #paginator
    paginator = Paginator(user_transactions, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj

    #Get information for navbar and form submission
    context["accounts"] = accounts

    #Get information for form submission 
    context["categories"] = sorted(Budget.CATEGORY_CHOICES)
    context["type_list"] = sorted(Transaction.TRANS_CHOICES)

    return render(request, 'budgets/transactions.html', context)


@login_required
def budgets(request, id):
    """
    User Bugget Page: 
    Add New Budget, View Budget Status
    """
    context = {}
    print(request.POST)

    if id != request.user.id:
        raise Http404

    if request.method == "POST":
        if 'AddBudget' in request.POST:
            form = BudgetForm(data=request.POST)
            if form.is_valid():
                add_budget(form, request.user)
   
        elif 'DeleteBudget' in request.POST:
            budget_pk = request.POST.get('DeleteBudget')
            delete_budget(budget_pk)

    # get a list of categories user does not have budgets set up for
    all_categories =  set([choice[0] for choice in Budget.CATEGORY_CHOICES])
    user_budgets = Budget.objects.filter(owner=request.user.id).order_by('category')
    categories_with_budget = sorted(set(user_budgets.values_list('category', flat=True)))
    categories_without_budget = list(all_categories.difference(categories_with_budget))
    context['categories_without_budget'] = sorted(categories_without_budget)

    #get details for user's month to dat budget status
    sum_of_user_budgets =  get_budget_mtd_information(user_budgets, request.user)
    context['sum_of_user_budgets'] = sum_of_user_budgets

    #Get information for navbar 
    context['accounts'] = Account.objects.filter(owner=request.user).order_by('nickname')

    return render(request, 'budgets/budgets.html', context)