#!/usr/bin/env python
import argparse
import sys

from engine.factories import TransactionFactory
from engine.file_manager import read_transactions_file
from engine.models import Account, InvalidTransactionException


def print_accounts_resume(accounts: dict[int, Account]):
    print('client, available, held, total, locked')
    for account in accounts.values():
        print(f'{account.account_id}, {account.available_funds}, {account.held_funds}, {account.total_funds}'
              f', {account.locked}')


def read_and_process_transactions(transactions_file: str) -> dict[int, Account]:
    accounts = {}
    for tx_type, account_id, tx_id, tx_amount in read_transactions_file(transactions_file):
        tx = TransactionFactory.create(tx_type, account_id, tx_id, tx_amount)

        if tx.account_id not in accounts:
            accounts[tx.account_id] = Account(tx.account_id)

        try:
            accounts[tx.account_id].tx_apply(tx)
        except InvalidTransactionException as e:
            print(f"An error has occurred while processing transaction {tx}. Details: {e}", file=sys.stderr)

    return accounts


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Payment Engine')
    arg_parser.add_argument('file', metavar='FILE', type=str, help='File with transactions')
    args = arg_parser.parse_args()

    accounts = read_and_process_transactions(args.file)
    print_accounts_resume(accounts)
