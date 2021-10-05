import os
from budgettracker.models import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expensetracket.settings")


def specific_umacs(user_id):
    print(budgettracker.models.UserMadeAccount.objects.get(id=user_id))
    return "Hello"



    """
    user = UserMadeAccount(
        UMA_user = ,
        UMA_name = ,
        UMA_type = ,
        UMA_balance = 
    )
    """

    
