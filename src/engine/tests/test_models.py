from decimal import Decimal

import pytest

from engine.models import Account, Transaction, InvalidTransactionException


@pytest.mark.parametrize("tx_id,is_valid", [
    (-1, False),
    ( 0, False),
    ( 1, True),
    (4294967295 - 1, True),
    (4294967295,     True),
    (4294967295 + 1, False),
])
def test_assert_valid_tx_id(tx_id: int, is_valid: bool):
    try:
        Transaction.assert_valid_tx_id(tx_id)
        assert True is is_valid
    except InvalidTransactionException as e:
        assert False is is_valid
        assert str(e) == f"Invalid tx_id: {tx_id}"


def test_transaction_cannot_be_created_with_invalid_tx_id():
    with pytest.raises(InvalidTransactionException):
        Transaction(tx_id=-1, account_id=1, tx_amount=Decimal('1.00'), tx_type=Transaction.TYPE_DEPOSIT)


def test_transaction_cannot_be_created_with_invalid_account_id():
    with pytest.raises(ValueError):
        Transaction(tx_id=1, account_id=-1, tx_amount=Decimal('1.00'), tx_type=Transaction.TYPE_DEPOSIT)


@pytest.mark.parametrize("account_id,is_valid", [
    (-1, False),
    ( 0, False),
    ( 1, True),
    (65535 - 1, True),
    (65535,     True),
    (65535 + 1, False),
])
def test_assert_valid_account_id(account_id: int, is_valid: bool):
    try:
        Account.assert_valid_account_id(account_id)
        assert True is is_valid
    except ValueError as e:
        assert False is is_valid
        assert str(e) == f"Invalid account_id: {account_id}"


def test_account_cannot_be_created_with_invalid_account_id():
    with pytest.raises(ValueError):
        Account(account_id=-1)

