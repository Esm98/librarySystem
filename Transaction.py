class Transaction:
    def __init__(self, user, item, transaction_type, date):
        self.user = user
        self.item = item
        self.transaction_type = transaction_type  # e.g., "checkout", "return"
        self.date = date

    # Additional methods to handle the transaction logic, if needed
