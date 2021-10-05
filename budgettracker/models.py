import os
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.core import serializers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expensetracker.settings")

class UserMadeAccount(models.Model):
    # UMA - UserMadeAccount
    UMA_user = models.ForeignKey(User, on_delete=models.CASCADE)
    UMA_name = models.CharField(max_length=100)
    UMA_type = models.CharField(max_length=100)
    UMA_balance = models.FloatField()

    def __str__(self):
        return self.UMA_name

class AccountTransactions(models.Model):
    AT_UMA = models.ForeignKey(UserMadeAccount, on_delete=models.CASCADE)
    AT_date = models.DateTimeField(auto_now=True)
    AT_description = models.TextField()
    AT_debit = models.FloatField()
    AT_credit = models.FloatField()

def specific_umacs(user_id):
    return UserMadeAccount.objects.filter(UMA_user=user_id)

def single_uma(account_id):
    for account in UserMadeAccount.objects.filter(id=account_id):
        return account

def uma_transactions(user_id, account_id):
    return AccountTransactions.objects.filter(AT_UMA=account_id).order_by('-AT_date')[:10]

def uma_transactions_buffer(user_id, account_id, starting_no, next_10):
    transaction_data = AccountTransactions.objects.filter(AT_UMA=account_id).order_by('-AT_date')
    list_of_10 = transaction_data[:starting_no]

    # When button is pressed

    list_of_10 = transaction_data[next_10:starting_no + next_10]
    next_10 += 10

    return list_of_10


def add_uma(uma_form, user_obj):
    # Add a new account made by the user
    uma = UserMadeAccount(
        UMA_name = uma_form.cleaned_data.get('UMA_form_name'),
        UMA_type = uma_form.cleaned_data.get('UMA_form_type'),
        UMA_balance = uma_form.cleaned_data.get('UMA_form_balance'),
        UMA_user = user_obj
    )
    uma.save()

def delete_uma(uda_form, user_obj):
    # Delete user made account
    AccountTransactions.objects.filter(AT_UMA=user_obj.id).delete()
    UserMadeAccount.objects.filter(UMA_user=user_obj.id).filter(id=uda_form.cleaned_data.get('UDA_name').id).delete()

def delete_all_UMA(user_id):
    all_UMA = specific_umacs(user_id=user_id)
    for account in all_UMA:
        AccountTransactions.objects.filter(AT_UMA=account.id).delete()
    UserMadeAccount.objects.filter(UMA_user=user_id).delete()
    
def add_uma_transaction(uma_obj, transaction_name, debit_value=0, credit_value=0):

    transaction = AccountTransactions(
        AT_UMA=uma_obj,
        AT_date=datetime.now(),
        AT_description=transaction_name,
        AT_debit=debit_value,
        AT_credit=credit_value
    )
    transaction.save()

def balance_update(uma_obj, current_balance, debit_value=0, credit_value=0):
    account = single_uma(account_id=uma_obj.id)
    account.UMA_balance = float(uma_obj.UMA_balance) - float(debit_value) + float(credit_value)
    account.save()

def transfer_funds(from_account, to_account, uma_obj, funds):
    from_uma = UserMadeAccount.objects.get(id=from_account)
    to_uma = UserMadeAccount.objects.get(id=to_account)

    from_uma.UMA_balance -= float(funds)
    to_uma.UMA_balance += float(funds)

    from_uma.save()
    to_uma.save()

    # Add fund transfer as a transaction for each of the accounts -->
    
    # Add debit transaction to from_account:
    add_uma_transaction(
        uma_obj=from_uma,
        transaction_name= f"Transfer of funds to: {to_uma.UMA_name}",
        debit_value=float(funds)
    )
    # Add credit transaction to to_account:
    add_uma_transaction(
        uma_obj=to_uma,
        transaction_name = f"Transfer of funds from: {from_uma.UMA_name}",
        credit_value=float(funds)
    )

