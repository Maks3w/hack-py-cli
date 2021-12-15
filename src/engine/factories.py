from decimal import Decimal

from engine.models import AbstractTransaction, Transaction, DisputeTransaction


class TransactionFactory:
    @staticmethod
    def create(tx_type: str, account_id: int, tx_id: int, tx_amount: Decimal | None) -> AbstractTransaction:
        match tx_type:
            case Transaction.TYPE_DEPOSIT | Transaction.TYPE_WITHDRAWAL:
                return Transaction(
                    tx_type=tx_type,
                    account_id=account_id,
                    tx_id=tx_id,
                    tx_amount=tx_amount,
                )
            case Transaction.TYPE_DISPUTE | Transaction.TYPE_RESOLVE_DISPUTE | Transaction.TYPE_CHARGEBACK:
                return DisputeTransaction(
                    tx_type=tx_type,
                    account_id=account_id,
                    dispute_tx_id=tx_id,
                )
            case _:
                raise NotImplementedError(f'Unknown transaction type: {tx_type}')
