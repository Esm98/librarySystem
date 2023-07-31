from datetime import datetime, timedelta
from faker import Faker
import random
import csv
from Item import Item
fake = Faker()

library_items = []
for _ in range(100):
    title = fake.catch_phrase()
    type = random.choice(["Book"])
    status = "available"
    due_date = None
    checkout_period = random.choice(["3 weeks", "2 weeks"])
    value = round(random.uniform(5.00, 30.00), 2)

    item = Item(title, type,status,due_date, checkout_period, value)
    library_items.append(item)

# Write to CSV file
    with open('libraryitems.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["Title", "Type", "Status", "DueDate", "CheckoutPeriod", "Value"])
            # Write the items
            for item in library_items:
                writer.writerow([item.title, item.type, item.status, item.due_date, item.checkout_period, item.value])