import pytest
from app.calculations import *

@pytest.fixture
def zero_bank_balance():
    return BankAcount()

@pytest.fixture
def bank_account():
    return BankAcount(50)

@pytest.mark.parametrize("x, y, result", [
    (3, 2, 5),
    (2, 3, 5),
    (1, 5, 6),
    (5, 6, 11)
])
def test_add(x, y, result):
    assert add(x, y) == result
    
def test_subtract():
    assert subtract(3, 1) == 2
    
def test_multiply():
    assert multiply(3, 2) == 6
    
def test_division():
    assert divide(16, 4) == 4
    
def test_initial_amount(bank_account):

    assert bank_account.balance == 50
    
def test_default_initial_amount(zero_bank_balance):

    assert zero_bank_balance.balance == 0
    
def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40
    
def test_deposit(bank_account):

    bank_account.deposit(10)
    assert bank_account.balance == 60
    
def test_interest(bank_account):
    bank_account.get_interest()
    assert round(bank_account.balance, 4) == 55