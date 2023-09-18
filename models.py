from sqlalchemy import create_engine, Column, Integer, String, DateTime, UniqueConstraint, TIMESTAMP, CHAR, DECIMAL, ForeignKey, CheckConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import json
import bcrypt

engine = create_engine


DATABASE_FILE = "users_db.json"

Base = declarative_base()

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email_address = Column(String(255), unique=True)
    phone_number = Column(String(20), unique=True)
    user_name = Column(String(50), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def __init__(self, first_name, last_name, email_address, phone_number, user_name):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.user_name = user_name

class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    account_no = Column(String(10), unique=True)
    balance = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='wallets')

    def __init__(self, user_id, account_no):
        self.user_id = user_id
        self.account_no = account_no

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    transaction_type = Column(String(10), CheckConstraint("transaction_type IN ('debit', 'credit')"))
    payment_purpose = Column(String(20), CheckConstraint("payment_purpose IN ('funding', 'transfer', 'airtime')"))
    transaction_reference = Column(CHAR(20), unique=True)
    status = Column(String(20), CheckConstraint("status IN ('failed', 'successful', 'pending')"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='transactions')

def __init__ (self, user_id, transaction_type, payment_purpose, transaction_reference, status):
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.payment_purpose = payment_purpose
        self.transaction_reference = transaction_reference
        self.status = status




def load_users():
    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(DATABASE_FILE, "w") as file:
        json.dump(users, file)


def create_account(username, password):
    users = load_users()

    if username in users:
        print("Username already exists.")
        return

    users[username] = {"password": password, "wallet": 0}
    save_users(users)
    print("Account created successfully.")


def authenticate(username, password):
    users = load_users()

    if username in users and users[username]["password"] == password:
        print("Authentication successful.")
        return True
    else:
        print("Invalid username or password.")
        return False


def get_wallet_balance(username):
    users = load_users()
    return users[username]["wallet"]


def create_transaction(username, amount):
    users = load_users()

    if username in users:
        if amount > 0:
            users[username]["wallet"] += amount
            save_users(users)
            print(f"Transaction successful. Wallet balance: {get_wallet_balance(username)}")
        else:
            print("Invalid transaction amount. Please enter a positive value.")
    else:
        print("User not found. Please create an account.")





def load_users():
    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(DATABASE_FILE, "w") as file:
        json.dump(users, file)

# Function to create a new account with hashed password
def create_account(username, password):
    users = load_users()

    if username in users:
        print("Username already exists.")
        return

  
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users[username] = {"password": hashed_password.decode('utf-8'), "wallet": 0}
    save_users(users)
    print("Account created successfully.")

# Function to authenticate a user
def authenticate(username, password):
    users = load_users()

    if username in users:
        stored_password = users[username]["password"]

        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print("Authentication successful.")
            return True

    print("Invalid username or password.")
    return False


# Main program
if __name__ == "__main__":
    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Create Transaction")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            create_account(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if authenticate(username, password):
                print(f"Wallet balance: {get_wallet_balance(username)}")
        elif choice == "3":
            username = input("Enter username: ")
            amount = float(input("Enter transaction amount: "))
            create_transaction(username, amount)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

