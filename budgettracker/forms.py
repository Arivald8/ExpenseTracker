from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelChoiceField
from .models import UserMadeAccount

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class UmaForm(forms.Form):
    # User Made Account
    UMA_form_name = forms.CharField(label="Account Name", max_length=100)
    UMA_form_type = forms.CharField(label="Account Type", max_length=100)
    UMA_form_balance = forms.FloatField(label="Balance")

class UdaForm(forms.Form):
    # User Deleted Account
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['UDA_name'].queryset = UserMadeAccount.objects.filter(UMA_user=user)

    UDA_name = forms.ModelChoiceField(label="Account", queryset=UserMadeAccount.objects.all())

class DebitForm(forms.Form):
    debit_name = forms.CharField(label="Expense", max_length=100, required=False)
    debit_value = forms.FloatField(label="Value", required=False)

class CreditForm(forms.Form):
    credit_name = forms.CharField(label="Income", max_length=100, required=False)
    credit_value = forms.FloatField(label="Value", required=False)

class TransferForm(forms.Form):
    # Transfer funds between user made accounts
    def __init__(self, *args, user, account, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.account = account
        self.fields['from_account'].queryset = UserMadeAccount.objects.filter(UMA_user=user)
        self.fields['to_account'].queryset = UserMadeAccount.objects.filter(UMA_user=user) #.exclude(id=account) 

    from_account = forms.ModelChoiceField(label="From account:", queryset=UserMadeAccount.objects.all())
    to_account = forms.ModelChoiceField(label="To account:", queryset=UserMadeAccount.objects.all())
    funds = forms.FloatField(label="Value")
    

    
