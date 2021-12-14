from decimal import Decimal


class Transaction:
    @classmethod
    def new_deposit(cls, account_id: int, tx_id: int, tx_amount: Decimal) -> 'Transaction':
        return cls(account_id, tx_id, Transaction.TYPE_DEPOSIT, tx_amount)

    @classmethod
    def new_withdrawal(cls, account_id: int, tx_id: int, tx_amount: Decimal) -> 'Transaction':
        return cls(account_id, tx_id, Transaction.TYPE_WITHDRAWAL, tx_amount)

    TYPE_DEPOSIT: str = 'deposit'
    TYPE_WITHDRAWAL: str = 'withdrawal'

    tx_id: int
    tx_type: str
    tx_amount: Decimal

    def __init__(self, account_id: int, tx_id: int, tx_type: str, tx_amount: Decimal):
        self.client_id = account_id
        self.tx_id = tx_id
        self.tx_type = tx_type
        self.tx_amount = tx_amount

    def __str__(self):
        return f"Transaction({self.client_id} {self.tx_id} {self.tx_type} {self.tx_amount})"

    def __repr__(self):
        return self.__str__()


class Account:
    account_id: int
    available_funds: Decimal
    total_funds: Decimal

    def __init__(self, account_id: int):
        self.account_id = account_id
        self.available_funds = Decimal('0.0000')
        self.total_funds = Decimal('0.0000')
        self.txs = []

    def tx_add(self, tx: Transaction) -> None:
        match tx.tx_type:
            case Transaction.TYPE_DEPOSIT:
                self._deposit(tx)
            case Transaction.TYPE_WITHDRAWAL:
                self._withdrawal(tx)
            case _:
                raise NotImplementedError(f'Unknown transaction type: {tx.tx_type}')

        self.txs.append(tx)

    def _deposit(self, tx: Transaction) -> None:
        self.available_funds += tx.tx_amount
        self.total_funds += tx.tx_amount

    def _withdrawal(self, tx: Transaction) -> None:
        if self.available_funds < tx.tx_amount:
            raise InsufficientAvailableFunds(self, tx)
        self.available_funds -= tx.tx_amount
        self.total_funds -= tx.tx_amount

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
