class InsufficientFunds(Exception):
    pass

def add(num1: int, num2: int):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1*num2

def divide(num1: int, num2: int):
    return num1/num2

class BankAcount():
    def __init__(self, initial_balance = 0) -> int:
        self.balance = initial_balance
        
    def withdraw(self, amount: int):
        if amount > self.balance:
            raise InsufficientFunds("Not sufficient balance withdraw")
        self.balance -= amount
        
    def deposit(self, amount: int):
        self.balance += amount
        
    def get_interest(self):
        self.balance *= 1.1