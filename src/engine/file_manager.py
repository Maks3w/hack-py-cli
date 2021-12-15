import csv
from decimal import Decimal


def read_transactions_file(file_path: str, skip_headers: bool = True) -> list:
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f)
        skip_headers and next(csv_reader, None)  # skip first line

        for row in csv_reader:
            tx_type = row[0].strip()
            account_id = int(row[1].strip())
            tx_id = int(row[2].strip())
            raw_amount = row[3].strip()
            tx_amount = Decimal(raw_amount) if raw_amount != '' else None

            yield tx_type, account_id, tx_id, tx_amount
