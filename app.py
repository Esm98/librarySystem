import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QLineEdit,QPushButton,QVBoxLayout,QWidget,QInputDialog,QComboBox,QDialog,QListWidget
from User import User
import csv
from Item import Item
from datetime import datetime, timedelta


class CheckoutWindow(QDialog):
    def __init__(self, items, user):
        super().__init__()
        self.items = items
        self.user = user
        layout = QVBoxLayout()

        # Item selection combo box
        self.item_combo_box = QComboBox()
        for item in items:
            if item.status == "available": # Only list available items
                self.item_combo_box.addItem(item.title)
        layout.addWidget(self.item_combo_box)

        # User selection combo box
        
        # Checkout button
        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout_item)
        layout.addWidget(self.checkout_button)

        self.setLayout(layout)

    def checkout_item(self):
        selected_title = self.item_combo_box.currentText()
        selected_user = self.user
        for item in self.items:
            if item.title == selected_title:
                print(f"Attempting to check out {selected_title}...") # Debug print
                if item.status == "available":
                    print("Item is available.") # Debug print
                else:
                    print("Item is not available.") # Debug print
                if selected_user.checkout_item(item):
                    print(f"{selected_title} has been checked out.")
                    self.update_csv()
                    self.update_users_csv(self.user)
                    item.status = "unavailable"
                else:
                    print("User unable to check out item.") # Debug print
                    print(f"An error occurred while checking out {selected_title}.")
                break


    


    def update_csv(self):
        with open('libraryitems.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Title", "Type", "Status", "DueDate", "CheckoutPeriod", "Value"])
            for item in self.items:
                # Assuming the attributes are structured this way; modify as needed
                writer.writerow([item.title, item.type, item.status, item.get_due_date(), item.checkout_period, item.value])

    def update_users_csv(self, user):
        with open('users.csv', 'r', newline='') as csvfile:
            # Read the existing users
            reader = csv.reader(csvfile)
            users = [row for row in reader]

        with open('users.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write headers
            writer.writerow(['Name', 'Address', 'PhoneNumber', 'LibraryCardNumber', 'Age', 'Password', 'CheckedOutItems'])
            # Write the existing users
            for row in users[1:]:
                if row[3] == str(user.library_card_number):  # Update the user with new checked-out items
                    # Combine existing and new checked-out items
                    existing_checked_out_items = row[6]
                    new_checked_out_items = user.get_checked_out_items_string()
                    combined_checked_out_items = existing_checked_out_items + ';' + new_checked_out_items
                    writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], combined_checked_out_items])
                else:
                    writer.writerow(row)







class ViewUsersWindow(QMainWindow):
    def __init__(self, users, library_app, parent=None):
        super().__init__(parent)
        self.users = users
        self.library_app = library_app
        self.parent = parent
        self.setWindowTitle("View Users")
        layout = QVBoxLayout()

        self.user_list_widget = QListWidget(self)
        for user_id, user in users.items():
            self.user_list_widget.addItem(str(user))
        layout.addWidget(self.user_list_widget)

        # Add a button to allow selection of a user
        self.select_user_button = QPushButton("Select User", self)
        self.select_user_button.clicked.connect(self.select_user)
        layout.addWidget(self.select_user_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_user(self):
        selected_user_text = self.user_list_widget.currentItem().text()
        selected_user_id = None
        selected_user = None
        for user_id, user in self.users.items():
            if str(user) == selected_user_text:
                selected_user_id = user_id
                selected_user = user
                break

        if selected_user_id is not None:
            items = self.library_app.items
            library_card_number = selected_user.library_card_number  # Assuming this attribute exists in the User class
            details_window = UserDetailsWindow(library_card_number, items)
            details_window.exec_()
            self.library_app.select_user(selected_user_id)
        else:
            print(f"Error: Could not find selected user.")
        self.close()


class UserDetailsWindow(QDialog):
    def __init__(self, user_library_card_number, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Details")
        layout = QVBoxLayout()
        checked_out_items = []
        checked_out_items = []
       
        with open('users.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) # Skip the header row
            for row in reader:
                if len(row) != 7:  # Check if the row has the correct number of values
                    print(f"Skipping row with incorrect number of values: {row}")
                    continue
               

                name, address, phone_number, library_card_number, age, password, checked_out_items_string = row
                

                if library_card_number == user_library_card_number:
                    checked_out_titles = checked_out_items_string.split(';')
                    checked_out_items = [item for item in items if item.title in checked_out_titles]
                    


                    break
            else: # No matching user found
                print(f"User with library card number {user_library_card_number} not found.")
                return
         
    
        # Name
        name_label = QLabel(f"Name: {name}")
        layout.addWidget(name_label)

        # Library Card Number
        card_number_label = QLabel(f"Library Card Number: {library_card_number}")
        layout.addWidget(card_number_label)

        # Checked Out Items
        checked_out_label = QLabel("Checked Out Items:")
        layout.addWidget(checked_out_label)
        checked_out_list = QListWidget(self)
        for item in checked_out_items:
            checked_out_list.addItem(item.title)
            print(f"Checked out items: {item.title}")
            
        layout.addWidget(checked_out_list)

        

        # OK Button
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.close)
        layout.addWidget(ok_button)

        self.setLayout(layout)




    
class EditUserWindow(QMainWindow):
    def __init__(self, users):
        super().__init__()
        self.users = users
        self.setWindowTitle("Edit User")
        # Here you can create a form similar to RegistrationWindow to edit user details

class DeleteUserWindow(QMainWindow):
    def __init__(self, users):
        super().__init__()
        self.users = users
        self.setWindowTitle("Delete User")
        # Here you can create a form to select a user to delete




class RegistrationWindow(QMainWindow):
    def __init__(self,main_app):
        super().__init__()
        self.setWindowTitle("Library System Registration")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.main_app = main_app
        self.name_input = QLineEdit(self)
        self.address_input = QLineEdit(self)
        self.phone_number_input = QLineEdit(self)
        self.library_card_number_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.age_input = QLineEdit(self)
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Address:"))
        layout.addWidget(self.address_input)
        layout.addWidget(QLabel("Phone Number:"))
        layout.addWidget(self.phone_number_input)
        layout.addWidget(QLabel("Library Card Number:"))
        layout.addWidget(self.library_card_number_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Age:):"))
        layout.addWidget(self.age_input)
        layout.addWidget(self.register_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def register_user(self):
        name = self.name_input.text()
        address = self.address_input.text()
        phone_number = self.phone_number_input.text()
        library_card_number = self.library_card_number_input.text()
        age = int(self.age_input.text())  # Assuming there's a field where users enter their age
        password = self.password_input.text()

        user = User.register(name, address, phone_number, library_card_number, age)

        # Add the user to a dictionary or other data structure
        self.main_app.users[library_card_number] = user
        self.main_app.passwords[library_card_number] = password

        print(f"User {name} registered with library card number {library_card_number}")

        # Save the updated users to the CSV file
        self.main_app.save_users_to_csv(user)

        self.close()



class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Library System Login")
        self.setGeometry(100, 100, 300, 200)

        

        self.Employee_ID_number_input = QLineEdit(self)
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.attempt_login)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide the password text

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter Employee ID:"))
        layout.addWidget(self.Employee_ID_number_input)
        

        layout.addWidget(QLabel("Enter Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        

    


    def attempt_login(self):
        employeeId = self.Employee_ID_number_input.text() # Fix the variable name here
        password = self.password_input.text()

        # Example list of valid credentials
        valid_credentials = {
            "": "",
            "": ""
        }
        if employeeId in valid_credentials and valid_credentials[employeeId] == password:
            self.accept_login(employeeId)
        else:
            print("Employee ID number or password")

    def accept_login(self,employeeId):
        print(f"Logged in with Employee Id: {employeeId}")
        self.main_window = LibraryApp(employeeId)  # Create the main window
        self.main_window.show()
        self.close()


class LibraryApp(QMainWindow):
    def __init__(self,employeeId):
        super().__init__()
        self.employeeId = employeeId
        # Set window properties
        self.setWindowTitle("Library System")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        # Add a label to the window
        label = QLabel('Welcome to the Library System', self)
        label.move(200, 250)
        label.move(150, 50) # Adjusted x coordinate for centering
        label.setFixedWidth(500) # Set fixed width to fit the text
        self.library_card_number = None
        self.users = {}
        self.passwords = {}
        self.transactions = []
        self.items = []

        self.checkout_window = CheckoutWindow(self.items, self.users)
    

        with open('users.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) # Skip the header
            for row in reader:
                if len(row) != 7:
                    print(f"Skipping row with incorrect number of values: {row}")
                    continue
                name, address, phone_number, library_card_number, age, password, checked_out_items_string = row
                checked_out_titles = checked_out_items_string.split(';')
                checked_out_items = [item for item in self.items if item.title in checked_out_titles]
                user = User.register(name, address, phone_number, library_card_number, int(age))
                user.checked_out_items = checked_out_items
                self.users[library_card_number] = user
                self.passwords[library_card_number] = password



        with open('libraryitems.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                print("Processing row:", row)  # Debug print statement
                checkout_period_str = row[4]
                checkout_period_weeks = int(checkout_period_str.split()[0])  # Extract the number of weeks
                item = Item(row[0], row[1], row[2], row[3], checkout_period_weeks, float(row[5]))
                self.items.append(item)


        self.user = self.users.get(self.library_card_number) if self.library_card_number else None
        if self.user is not None:
            self.fines_label = QLabel(f"Current fines: ${self.user.fines:.2f}")  # Display fines
            layout.addWidget(self.fines_label)
        else:
            # Handle the case where the user is not found
            print(f"Error: User with library card number {self.library_card_number} not found.")
            # You might want to redirect the user back to the login page or show an error message
        
        

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.open_registration_window)
        
        self.view_users_button = QPushButton("View Users", self)
        self.view_users_button.clicked.connect(self.open_view_users_window)
        self.edit_user_button = QPushButton("Edit User", self)
        self.edit_user_button.clicked.connect(self.open_edit_user_window)
        self.delete_user_button = QPushButton("Delete User", self)
        self.delete_user_button.clicked.connect(self.open_delete_user_window)
        self.checkout_button = QPushButton("Checkout Item", self)
        self.checkout_button.clicked.connect(self.open_checkout_window)

        self.view_users_details_button = QPushButton("View user details", self)
        self.view_users_details_button.clicked.connect(self.view_user_details)

        layout.addWidget(self.register_button)

        
        layout.addWidget(self.view_users_button)

      
        layout.addWidget(self.edit_user_button)

        
        layout.addWidget(self.delete_user_button)

        layout.addWidget(self.checkout_button)

        layout.addWidget(self.view_users_details_button)

        container = QWidget()  # Create a container widget
        container.setLayout(layout)  # Set the layout of the container widget
        self.setCentralWidget(container)  # Set the central widget of the main window

        self.show()


    def view_user_details(self):
        selected_library_card_number = self.select_user(self.user) # Replace with your method to get the selected user's library card number
        items = self.items # Assuming this holds the list of Item objects
        details_window = UserDetailsWindow(selected_library_card_number, items)
        details_window.exec_()

    def select_user(self, user_id):
        self.user = self.users.get(user_id)
        if self.user:
            print(f"Selected user with library card number {user_id}")
        else:
            print(f"Error: User with library card number {user_id} not found.")

    def open_checkout_window(self):
        self.checkout_window = CheckoutWindow(self.items, self.user)
        self.checkout_window.show()

    def open_view_users_window(self):
        self.view_users_window = ViewUsersWindow(self.users,self)
        self.view_users_window.show()

    def open_edit_user_window(self):
        self.edit_user_window = EditUserWindow(self.users)
        self.edit_user_window.show()

    def open_delete_user_window(self):
        self.delete_user_window = DeleteUserWindow(self.users)
        self.delete_user_window.show()

    def open_registration_window(self):
        self.registration_window = RegistrationWindow(self)
        self.registration_window.show()

    def register_user(self):
        name = self.name_input.text()
        address = self.address_input.text()
        phone_number = self.phone_number_input.text()
        library_card_number = self.library_card_number_input.text()
        age = int(input("Enter your age: ")) # Ask for the user's actual age

        password = self.password_input.text()

        # You'll probably want to add some validation and error handling here

        user = User.register(name, address, phone_number, library_card_number, age)
        print(f"Welcome, {user.name}! Your registration is complete.")

        # Add the user to a dictionary or other data structure
        self.users[library_card_number] = user
        self.passwords[library_card_number] = password

        with open('users.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header
            writer.writerow(['Name', 'Address', 'PhoneNumber', 'LibraryCardNumber', 'Age', 'CheckedOutItems'])
            for user in self.users:
                checked_out_items_string = user.get_checked_out_items_string()
                writer.writerow([user.name, user.address, user.phone_number, user.library_card_number, user.age, checked_out_items_string])


        print(f"User {name} registered with library card number {library_card_number}")
        self.close()

    def save_users_to_csv(self, user):
        with open('users.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            library_card_number = user.library_card_number
            writer.writerow([user.name, user.address, user.phone_number, library_card_number, user.age, self.passwords[library_card_number]])
            #for user_id, user in self.users.items():
                #writer.writerow([user.name, user.address, user.phone_number, user_id, user.age, self.passwords[user_id]])
    def load_users_from_csv(self):
        try:
            with open('users.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header row
                for row in reader:
                    name, address, phone_number, library_card_number, age, password = row
                    user = User.register(name, address, phone_number, library_card_number, int(age))
                    self.users[library_card_number] = user
                    self.passwords[library_card_number] = password
        except FileNotFoundError:
            print("No users file found. Starting with an empty user list.")


    

 

    def add_user(self, user, password):
        library_card_number = user.library_card_number
        self.users[library_card_number] = user
        self.passwords[library_card_number] = password

    def view_users(self):
        for user in self.users.values():
            print(user)

    def edit_user(self, library_card_number, new_data):
        user = self.users.get(library_card_number)
        if user:
            pass
            # Update user attributes based on new_data
            # ...

    def delete_user(self, library_card_number):
        if library_card_number in self.users:
            del self.users[library_card_number]

    

    def pay_fines_dialog(self):
        amount, ok = QInputDialog.getDouble(self, 'Pay Fines', 'Enter amount to pay:')
        if ok:
            self.user.pay_fine(amount)
            self.fines_label.setText(f"Current fines: ${self.user.fines:.2f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
