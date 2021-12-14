from abc import ABCMeta
from decimal import Decimal


class AbstractTransaction(metaclass=ABCMeta):
    @classmethod
    def new_deposit(cls, account_id: int, tx_id: int, tx_amount: Decimal) -> 'Transaction':
        return Transaction(account_id, tx_id, Transaction.TYPE_DEPOSIT, tx_amount)

    @classmethod
    def new_withdrawal(cls, account_id: int, tx_id: int, tx_amount: Decimal) -> 'Transaction':
        return Transaction(account_id, tx_id, Transaction.TYPE_WITHDRAWAL, tx_amount)

    @classmethod
    def new_dispute(cls, account_id: int, tx_under_dispute_id: int) -> 'DisputeTransaction':
        return DisputeTransaction(account_id, Transaction.TYPE_DISPUTE, tx_under_dispute_id)

    @classmethod
    def new_resolve_dispute(cls, account_id: int, tx_under_dispute_id: int) -> 'DisputeTransaction':
        return DisputeTransaction(account_id, Transaction.TYPE_RESOLVE_DISPUTE, tx_under_dispute_id)

    @classmethod
    def new_chargeback(cls, account_id: int, tx_under_dispute_id: int) -> 'DisputeTransaction':
        return DisputeTransaction(account_id, Transaction.TYPE_CHARGEBACK, tx_under_dispute_id)

    TYPE_DEPOSIT: str = 'deposit'
    TYPE_WITHDRAWAL: str = 'withdrawal'
    TYPE_DISPUTE: str = 'dispute'
    TYPE_RESOLVE_DISPUTE: str = 'resolve'
    TYPE_CHARGEBACK: str = 'chargeback'

    account_id: int
    tx_type: str

    def __init__(self, account_id: int, tx_type: str):
        Account.assert_valid_account_id(account_id)
        self.account_id = account_id
        self.tx_type = tx_type

    def __repr__(self):
        return self.__str__()


class Transaction(AbstractTransaction):
    @staticmethod
    def assert_valid_tx_id(tx_id: int) -> None:
        # Assert number range match with Rust u32 [0, 2^32)
        if tx_id < 1 or tx_id > 4294967295:
            raise InvalidTransactionException(f'Invalid tx_id: {tx_id}')

    tx_id: int
    tx_amount: Decimal

    def __init__(self, account_id: int, tx_id: int, tx_type: str, tx_amount: Decimal):
        super().__init__(account_id, tx_type)
        Transaction.assert_valid_tx_id(tx_id)
        self.tx_id = tx_id
        self.tx_amount = tx_amount

    def __str__(self):
        return f"Transaction({self.account_id} {self.tx_id} {self.tx_type} {self.tx_amount})"


class DisputeTransaction(AbstractTransaction):
    def __init__(self, account_id: int, tx_type: str, dispute_tx_id: int):
        super().__init__(account_id, tx_type)
        Transaction.assert_valid_tx_id(dispute_tx_id)
        self.dispute_tx_id = dispute_tx_id

    def __str__(self):
        return f"Dispute({self.account_id} {self.tx_type} {self.dispute_tx_id})"


class Account:
    @staticmethod
    def assert_valid_account_id(account_id: int) -> None:
        # Assert number range match with Rust u16 [0, 2^16)
        if account_id < 1 or account_id > 65535:
            raise ValueError(f'Invalid account_id: {account_id}')

    account_id: int
    held_funds: Decimal
    total_funds: Decimal
    locked: bool

    @property
    def available_funds(self) -> Decimal:
        return self.total_funds - self.held_funds

    def __init__(self, account_id: int):
        Account.assert_valid_account_id(account_id)
        self.account_id = account_id
        self.held_funds = Decimal('0.0000')
        self.total_funds = Decimal('0.0000')
        self.locked = False
        self.txs = []

    def tx_add(self, tx: AbstractTransaction) -> None:
        match tx.tx_type:
            case Transaction.TYPE_DEPOSIT:
                self._deposit(tx)
            case Transaction.TYPE_WITHDRAWAL:
                self._withdrawal(tx)
            case Transaction.TYPE_DISPUTE:
                self._dispute(tx)
            case Transaction.TYPE_RESOLVE_DISPUTE:
                self._resolve_dispute(tx)
            case Transaction.TYPE_CHARGEBACK:
                self._chargeback(tx)
            case _:
                raise NotImplementedError(f'Unknown transaction type: {tx.tx_type}')

        self.txs.append(tx)

    def _deposit(self, tx: Transaction) -> None:
        self.total_funds += tx.tx_amount

    def _withdrawal(self, tx: Transaction) -> None:
        if self.available_funds < tx.tx_amount:
            raise InsufficientAvailableFunds(self, tx)
        self.total_funds -= tx.tx_amount

    def _dispute(self, tx: DisputeTransaction) -> None:
        self.held_funds += 0

    def _resolve_dispute(self, tx: DisputeTransaction) -> None:
        self.held_funds -= 0

    def _chargeback(self, tx: DisputeTransaction) -> None:
        self.locked = True
        self.held_funds -= 0
        self.total_funds -= 0

    def __str__(self):
        return f'Account({self.account_id}, {self.total_funds})'

    def __repr__(self):
        return self.__str__()


class InvalidTransactionException(ValueError):
    pass


class InsufficientAvailableFunds(InvalidTransactionException):
    def __init__(self, account: Account, tx: Transaction):
        self.account = account
        self.tx = tx

    def __str__(self):
        return f"Insufficient available funds"
