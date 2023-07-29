import csv
from faker import Faker

fake = Faker()

book_titles = [fake.catch_phrase() for _ in range(100)]  # Generates 100 fake titles

# You can then write these titles to a CSV file if needed:
with open('book_titles.csv', 'w', encoding='utf-8') as file:
    for title in book_titles:
        file.write(title + '\n')


def load_titles(filename):
    titles = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            titles.append(row[0])
    return titles

filename = 'libraryitems.csv'
book_titles = load_titles(filename)
for title in book_titles:
    print(title)  # Add to your system as needed
