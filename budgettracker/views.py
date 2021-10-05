from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from budgettracker.tests import TestUMA
from budgettracker.forms import CustomUserCreationForm, UmaForm, UdaForm, DebitForm, CreditForm, TransferForm
from budgettracker.models import specific_umacs, single_uma, add_uma, delete_uma, delete_all_UMA, UserMadeAccount, uma_transactions, add_uma_transaction, balance_update, transfer_funds

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
            login(request, user)

            return render(
                request, "register.html",
                {"form": CustomUserCreationForm}
            )
        else:
            print(form)
            return render(
                request, "logged_out.html"
            )

def logged_out(request):
    return render(request, 'logged_out.html')

def logged_in(request):
    return render(request, 'logged_in.html')

def user_accounts(request, user_id):
    # Alerts
    delete_all_accounts_alert = False # User is trying to delete all created accounts

    if request.user.is_authenticated:
        # Get all accounts of user by matching user_id
        user_made_accounts = specific_umacs(user_id)
        user_data = [i for i in user_made_accounts]

        # If user is creating an account -->
        if "UMA_form_name" in request.POST:
            if request.method == 'POST':
                uma_form = UmaForm(request.POST)
                uda_form = UdaForm(user=request.user)
                if uma_form.is_valid():

                    # Adds new user made account to the DB
                    add_uma(uma_form, request.user)

                    # Get all accounts of user by matching user_id
                    user_made_accounts = specific_umacs(user_id)
                    user_data = [i for i in user_made_accounts]   
                    return render(request, 'user_accounts.html', {"uma_form": uma_form, "uda_form": uda_form, "user_data": user_data})       
                    
        # If user is deleting an account -->
        if "UDA_name" in request.POST:
            if request.method == 'POST':

                uda_form = UdaForm(request.POST, user=request.user)
                uma_form = UmaForm()

                if uda_form.is_valid():

                    # Delete user made account from DB
                    delete_uma(uda_form=uda_form, user_obj=request.user)
                    
                    # Get all accounts of user by matching user_id
                    user_made_accounts = specific_umacs(user_id)
                    user_data = [i for i in user_made_accounts] 
                    return render(request, 'user_accounts.html', {"uma_form": uma_form, "uda_form": uda_form, "user_data": user_data})

        if request.method == 'GET':
            uma_form = UmaForm()
            uda_form = UdaForm(user=request.user)
        else:
            uma_form = UmaForm()
            uda_form = UdaForm(user=request.user)

        return render(request, 'user_accounts.html', {"uma_form": uma_form, "uda_form": uda_form, "user_data": user_data})
    else:
        return render(request, 'please_authenticate.html')

def specific_uma(request, uma_id):
    # Alerts
    same_account_transfer_alert = False # Fund transfer between the same account alert
    invalid_balance_alert = False # Not enough funds in an account to perform an action

    # Get initial state of the account
    account_name = single_uma(account_id=uma_id).UMA_name
    transaction_data = uma_transactions(user_id=request.user.id, account_id=uma_id)
    account_balance = single_uma(account_id=uma_id).UMA_balance
    rounded_balance = round(account_balance, 2)
    
    # Form instantiations 
    debit_form = DebitForm()
    credit_form = CreditForm()
    transfer_form=TransferForm(user=request.user, account=uma_id)

    if request.method == "POST":
        # Adding debit -->
        if "debit_name" in request.POST:
            debit_form = DebitForm(request.POST)

            if debit_form.is_valid():
                
                # Get a specific account object to use as a FK when adding a transaction
                specific_account_obj = single_uma(account_id=uma_id)

                add_uma_transaction(
                    uma_obj=specific_account_obj,
                    transaction_name=debit_form.data['debit_name'],
                    debit_value=debit_form.data['debit_value']
                )

                # Reflect changes in the balance
                balance_update(
                    uma_obj=specific_account_obj,
                    current_balance=account_balance,
                    debit_value=debit_form.data['debit_value']
                )

                # Get most current state from specific user account before returning the template
                transaction_data = uma_transactions(user_id=request.user.id, account_id=uma_id)
                account_balance = single_uma(account_id=uma_id).UMA_balance
                rounded_balance = round(account_balance, 2)

                return render(request, 'specific_uma.html', 
                    {
                        "transaction_data": transaction_data, 
                        "debit_form": debit_form, 
                        "credit_form": credit_form, 
                        "account_balance": rounded_balance,
                        "transfer_form": transfer_form,
                        "account_name": account_name    
                    }
                )
            
        # Adding credit -->
        if "credit_name" in request.POST:
            credit_form = CreditForm(request.POST)

            if credit_form.is_valid():

                # Get a specific account object to use as a FK when adding a transaction
                specific_account_obj = single_uma(account_id=uma_id)

                add_uma_transaction(
                    uma_obj=specific_account_obj,
                    transaction_name=credit_form.data['credit_name'],
                    credit_value=credit_form.data['credit_value']
                )

                # Reflect changes in the balance
                balance_update(
                    uma_obj=specific_account_obj,
                    current_balance=account_balance,
                    credit_value=credit_form.data['credit_value']
                )

                # Get most current state from specific user account before returning the template
                transaction_data = uma_transactions(user_id=request.user.id, account_id=uma_id)
                account_balance = single_uma(account_id=uma_id).UMA_balance
                rounded_balance = round(account_balance, 2)

                return render(request, 'specific_uma.html', 
                    {
                        "transaction_data": transaction_data, 
                        "debit_form": debit_form, 
                        "credit_form": credit_form, 
                        "account_balance": rounded_balance, 
                        "transfer_form": transfer_form,
                        "account_name": account_name 
                    }
                )
   
        # Fund transfer -->
        if "from_account" in request.POST:
            transfer_form = TransferForm(request.POST, user=request.user, account=uma_id)

            if transfer_form.is_valid():

                # Validation -->

                # Check if user is trying to transfer between the same account
                if transfer_form.data['from_account'] == transfer_form.data['to_account']:
                    same_account_transfer_alert  = True
                    return render(request, 'specific_uma.html', 
                        {
                            "transaction_data": transaction_data, 
                            "debit_form": debit_form, 
                            "credit_form": credit_form, 
                            "account_balance": rounded_balance, 
                            "transfer_form": transfer_form,
                            "same_account_transfer_alert": same_account_transfer_alert,
                            "invalid_balance_alert": invalid_balance_alert,
                            "account_name": account_name 
                        }
                    )

                # Check if from_account has enough funds to transfer
                elif single_uma(account_id=uma_id).UMA_balance < float(transfer_form.data['funds']):
                    invalid_balance_alert = True   
                    return render(request, 'specific_uma.html', 
                        {
                            "transaction_data": transaction_data, 
                            "debit_form": debit_form, 
                            "credit_form": credit_form, 
                            "account_balance": rounded_balance, 
                            "transfer_form": transfer_form,
                            "same_account_transfer_alert": same_account_transfer_alert,
                            "invalid_balance_alert": invalid_balance_alert,
                            "account_name": account_name 
                        }
                    )
                # Validation Successfull -->
                else:          
                    transfer_funds(
                        from_account=transfer_form.data['from_account'],
                        to_account=transfer_form.data['to_account'],
                        uma_obj=single_uma(account_id=uma_id),
                        funds=transfer_form.data['funds']
                    )

                    # Fetch most recent account data before returning
                    transaction_data = uma_transactions(user_id=request.user.id, account_id=uma_id)
                    account_balance = single_uma(account_id=uma_id).UMA_balance
                    rounded_balance = round(account_balance, 2)
                    

                    return render(request, 'specific_uma.html', 
                        {
                            "transaction_data": transaction_data, 
                            "debit_form": debit_form, 
                            "credit_form": credit_form, 
                            "account_balance": rounded_balance, 
                            "transfer_form": transfer_form,
                            "same_account_transfer_alert": same_account_transfer_alert,
                            "invalid_balance_alert": invalid_balance_alert,
                            "account_name": account_name 
                        }
                    )


    
    return render(request, 'specific_uma.html', 
        {
            "transaction_data": transaction_data, 
            "debit_form": debit_form, 
            "credit_form": credit_form, 
            "account_balance": rounded_balance, 
            "transfer_form": transfer_form,
            "same_account_transfer_alert": same_account_transfer_alert,
            "invalid_balance_alert": invalid_balance_alert,
            "account_name": account_name
        }
    )

def specific_uma_transaction_buffer(request, uma_id, buffer_iteration):
    print(buffer_iteration)
    return render(request, 'specific_uma_transaction_buffer.html',
        {

        }
    )

def please_authenticate(request):
    pass

def delete_all_accounts(request, user_id):
    delete_all_UMA(user_id)
    return render(request, "delete_all_accounts.html")

def run_tests(request):
    DELETE_TEST = False

    if DELETE_TEST:
        pass

    else:
        tester = TestUMA(user=request.user)
        tester.create_umacs()
        tester.populate_umacs()

        return render(request, 'run_tests.html')
    
