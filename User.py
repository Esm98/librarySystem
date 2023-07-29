from Item import Item
class User:
    def __init__(self, name, address, phone_number, library_card_number,age):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.library_card_number = library_card_number
        self.age = age
        self.fines = 0
        
        self.checked_out_items = []
        self.requested_items = []


    def __str__(self):
        return f"Name: {self.name}, Library Card Number: {self.library_card_number}, Fines: ${self.fines:.2f}"

    @property
    def is_adult(self):
        return self.age > 12

    @classmethod
    def register(cls, name, address, phone_number, library_card_number, age):
        return cls(name, address, phone_number, library_card_number, age)

    def login(self):
        pass

    def checkout_item(self, Item):
          # Check if user is a child and has reached the maximum check out limit
        if self.age <= 12 and len(self.checked_out_items) >= 5:
            print(f"Children can check out a maximum of five items. Cannot checkout item: {Item.title}")
            return
        
        if Item.checkout():
            self.checked_out_items.append(Item)
        else:
            print(f"Cannot checkout item: {Item.title}")
        

    

    def request_item(self, Item):
        if Item.get_status() == "available":
            print("Item is available; you can check it out.")
        else:
            self.requested_items.append(Item)
            print(f"You've requested the item: {Item.title}")

    def renew_item(self, Item):
        if Item in self.checked_out_items and Item not in self.requested_items:
            Item.checkout() # Renew by checking out again
            print(f"You've renewed the item: {Item.title}")
        else:
            print("Cannot renew the item.")

    def add_fine(self, fine_amount):
        self.fines += fine_amount

    def pay_fine(self, amount):
        self.fines -= amount

    def display_fines(self):
        print(f"{self.name} has ${self.fines:.2f} in overdue fines.")

    def return_item(self, Item):
        if Item.is_overdue():
            fine_amount = Item.calculate_overdue_fine()
            self.add_fine(fine_amount)
            print(f"Item {Item.title} is overdue. A fine of ${fine_amount:.2f} has been added to your account.")
        Item.return_item()
        self.checked_out_items.remove(Item)
