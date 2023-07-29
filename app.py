import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QLineEdit,QPushButton,QVBoxLayout,QWidget,QInputDialog
from User import User

class ViewUsersWindow(QMainWindow):
    def __init__(self, users):
        super().__init__()
        self.setWindowTitle("View Users")
        layout = QVBoxLayout()
        for user in users.values():
            layout.addWidget(QLabel(str(user)))
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
        age = int(self.age_input.text()) # Assuming there's a field where users enter their age
        password = self.password_input.text()

        user = User.register(name, address, phone_number, library_card_number, age)
        
        # Add the user to a dictionary or other data structure
        self.main_app.users[library_card_number] = user
        self.main_app.passwords[library_card_number] = password

        print(f"User {name} registered with library card number {library_card_number}")
        self.close()




class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library System Login")
        self.setGeometry(100, 100, 300, 200)

        

        self.library_card_number_input = QLineEdit(self)
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.attempt_login)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide the password text

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter Library Card Number:"))
        layout.addWidget(self.library_card_number_input)
        

        layout.addWidget(QLabel("Enter Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        

    


    def attempt_login(self):
        library_card_number = self.library_card_number_input.text()
        password = self.password_input.text()

        # Example list of valid credentials
        valid_credentials = {
            "12345": "password",
            "67890": "password"
        }
        if library_card_number in valid_credentials and valid_credentials[library_card_number] == password:
            self.accept_login(library_card_number)
        else:
            print("Invalid library card number or password")

    def accept_login(self, library_card_number):
        print(f"Logged in with library card number: {library_card_number}")
        self.main_window = LibraryApp(library_card_number)  # Create the main window
        self.main_window.show()
        self.close()


class LibraryApp(QMainWindow):
    def __init__(self,library_card_number):
        super().__init__()
        self.library_card_number = library_card_number
        # Set window properties
        self.setWindowTitle("Library System")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        # Add a label to the window
        label = QLabel('Welcome to the Library System', self)
        label.move(200, 250)
        label.move(150, 50) # Adjusted x coordinate for centering
        label.setFixedWidth(500) # Set fixed width to fit the text

        self.users = {}
        self.passwords = {}
        self.transactions = []

        self.user = self.users.get(library_card_number)  # Get the current user
        if self.user is not None:
            self.fines_label = QLabel(f"Current fines: ${self.user.fines:.2f}")  # Display fines
            layout.addWidget(self.fines_label)
        else:
            # Handle the case where the user is not found
            print(f"Error: User with library card number {library_card_number} not found.")
            # You might want to redirect the user back to the login page or show an error message
        
        

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.open_registration_window)
        
        self.view_users_button = QPushButton("View Users", self)
        self.view_users_button.clicked.connect(self.open_view_users_window)
        self.edit_user_button = QPushButton("Edit User", self)
        self.edit_user_button.clicked.connect(self.open_edit_user_window)
        self.delete_user_button = QPushButton("Delete User", self)
        self.delete_user_button.clicked.connect(self.open_delete_user_window)

        
        layout.addWidget(self.register_button)

        
        layout.addWidget(self.view_users_button)

      
        layout.addWidget(self.edit_user_button)

        
        layout.addWidget(self.delete_user_button)

        container = QWidget()  # Create a container widget
        container.setLayout(layout)  # Set the layout of the container widget
        self.setCentralWidget(container)  # Set the central widget of the main window

        self.show()

    

    def open_view_users_window(self):
        self.view_users_window = ViewUsersWindow(self.users)
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

        print(f"User {name} registered with library card number {library_card_number}")
        self.close()

   


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
