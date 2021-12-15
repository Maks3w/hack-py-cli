from decimal import Decimal

from engine.file_manager import read_transactions_file
from engine.factories import TransactionFactory
from engine.models import Transaction, DisputeTransaction


def test_read_transactions_file():
    txs = []
    for tx_type, account_id, tx_id, tx_amount in read_transactions_file('asset/transactions_demo.csv'):
        txs.append(TransactionFactory.create(tx_type, account_id, tx_id, tx_amount))

    assert len(txs) == 8

    tx = txs[0]
    assert isinstance(tx, Transaction)
    assert tx.tx_type == 'deposit'
    assert tx.account_id == 1
    assert tx.tx_id == 1
    assert tx.tx_amount == Decimal('1.0')

    tx = txs[1]
    assert isinstance(tx, Transaction)
    assert tx.tx_type == 'deposit'
    assert tx.account_id == 2
    assert tx.tx_id == 2
    assert tx.tx_amount == Decimal('2.0')

    tx = txs[2]
    assert isinstance(tx, Transaction)
    assert tx.tx_type == 'deposit'
    assert tx.account_id == 1
    assert tx.tx_id == 3
    assert tx.tx_amount == Decimal('2.0')

    tx = txs[3]
    assert isinstance(tx, Transaction)
    assert tx.tx_type == 'withdrawal'
    assert tx.account_id == 1
    assert tx.tx_id == 4
    assert tx.tx_amount == Decimal('1.5')

    tx = txs[4]
    assert isinstance(tx, Transaction)
    assert tx.tx_type == 'withdrawal'
    assert tx.account_id == 2
    assert tx.tx_id == 5
    assert tx.tx_amount == Decimal('3.0')

    tx = txs[5]
    assert isinstance(tx, DisputeTransaction)
    assert tx.tx_type == 'dispute'
    assert tx.account_id == 1
    assert tx.dispute_tx_id == 1

    tx = txs[6]
    assert isinstance(tx, DisputeTransaction)
    assert tx.tx_type == 'resolve'
    assert tx.account_id == 1
    assert tx.dispute_tx_id == 1

    tx = txs[7]
    assert isinstance(tx, DisputeTransaction)
    assert tx.tx_type == 'chargeback'
    assert tx.account_id == 1
    assert tx.dispute_tx_id == 1
