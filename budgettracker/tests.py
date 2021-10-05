from django.test import TestCase
import budgettracker.forms, budgettracker.models
import random

class TestUMA:

    def __init__(self, user):

        self.names = [
            "Adam",
            "Super",
            "The Mormal",
            "Other",
            "Trip Saving",
            "Holiday",
            "Birthday",
            "Events",
            "BBQ",
            "The Secret",
            "Road Trip",
            "Test",
            "Damian",
        ]

        self.types = [
            "Normal",
            "Extra",
            "Premium",
            "Savings",
            "Investment",
            "Billing",
            "Other",
        ]

        self.user = user

        
    def create_umacs(self):
        print("USER: #########################")
        print(self.user)
        print("END USER ######################")
        NUM_OF_ACCOUNTS = 10

        for _ in range(NUM_OF_ACCOUNTS):
            # Add a new account made by the user
            uma = budgettracker.models.UserMadeAccount(
                UMA_name = random.choice(self.names),
                UMA_type = random.choice(self.types),
                UMA_balance = random.randint(0, 50000),
                UMA_user = self.user
            )
            uma.save()

    def populate_umacs(self):
        NUM_OF_TRANSACTIONS = 10

        accounts = budgettracker.models.specific_umacs(self.user.id)
        for account in accounts:
            for _ in range(NUM_OF_TRANSACTIONS):
                budgettracker.models.add_uma_transaction(
                    uma_obj=account,
                    transaction_name="Demo Transaction",
                    debit_value=random.randint(0, 5000),
                    credit_value=random.randint(0, 10000)
                )
