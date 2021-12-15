from decimal import Decimal

from engine.factories import TransactionFactory
from engine.models import Transaction, DisputeTransaction


def test_transaction_factory_deposit():
    row = ['deposit', 1, 1, Decimal('1.0')]

    transaction = TransactionFactory.create(*row)

    assert isinstance(transaction, Transaction)

    assert transaction.tx_type == 'deposit'
    assert transaction.account_id == 1
    assert transaction.tx_id == 1
    assert transaction.tx_amount == Decimal('1.0')


def test_transaction_factory_withdrawal():
    row = ['withdrawal', 1, 4, Decimal('1.5')]

    transaction = TransactionFactory.create(*row)

    assert isinstance(transaction, Transaction)

    assert transaction.tx_type == 'withdrawal'
    assert transaction.account_id == 1
    assert transaction.tx_id == 4
    assert transaction.tx_amount == Decimal('1.5')


def test_transaction_factory_dispute():
    row = ['dispute', 1, 4, None]

    transaction = TransactionFactory.create(*row)

    assert isinstance(transaction, DisputeTransaction)

    assert transaction.tx_type == 'dispute'
    assert transaction.account_id == 1
    assert transaction.dispute_tx_id == 4


def test_transaction_factory_resolve():
    row = ['resolve', 1, 4, None]

    transaction = TransactionFactory.create(*row)

    assert isinstance(transaction, DisputeTransaction)

    assert transaction.tx_type == 'resolve'
    assert transaction.account_id == 1
    assert transaction.dispute_tx_id == 4


def test_transaction_factory_chargeback():
    row = ['chargeback', 1, 4, None]

    transaction = TransactionFactory.create(*row)

    assert isinstance(transaction, DisputeTransaction)

    assert transaction.tx_type == 'chargeback'
    assert transaction.account_id == 1
    assert transaction.dispute_tx_id == 4
