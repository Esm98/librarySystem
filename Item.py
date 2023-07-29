from datetime import datetime, timedelta
class Item:
    def __init__(self, title, type, status, due_date, checkout_period,value):
        self.title = title
        self.type = type
        self.status = "available"
        self.due_date = None
        self.checkout_period = checkout_period
        self.value = value

    def checkout(self):
        if self.status == "available":
            self.status = "checked out"
            self.due_date = datetime.now() + timedelta(weeks=self.checkout_period)
            # Handle specific checkout periods
            if self.type == "bestseller":
                self.due_date = datetime.now() + timedelta(weeks=2)
            elif self.type == "audio/video":
                self.due_date = datetime.now() + timedelta(weeks=2)
            else:
                self.due_date = datetime.now() + timedelta(weeks=3)
                
            return True
        else:
            print(f"Item {self.title} is not available for checkout.")
            return False

    def get_status(self):
        return self.status

    def get_due_date(self):
        return self.due_date.strftime("%Y-%m-%d") if self.due_date else "Not checked out"
    
    def is_overdue(self):
        return datetime.now() > self.due_date if self.due_date else False

    def calculate_overdue_fine(self):
        if self.is_overdue():
            overdue_days = (datetime.now() - self.due_date).days
            fine_amount = overdue_days * 0.10 # Ten cents per day
            return min(fine_amount, self.value) # Assuming value is the item's value; fine won't exceed it
        else:
            return 0

class ReferenceMaterial(Item): # Note that Item is in parentheses
    def __init__(self, title, type, status, due_date, checkout_period, in_library_use_only):
        super().__init__(title, type, status, due_date, checkout_period) # Call the constructor of the parent class
        self.in_library_use_only = True

    def in_library_use(self):
        print(f"Reference material {self.title} cannot be checked out.")
