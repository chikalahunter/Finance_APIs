import json

# Initialize the database file
DATABASE_FILE = "users_db.json"

# Function to load user data from file
def load_users():
    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save user data to file
def save_users(users):
    with open(DATABASE_FILE, "w") as file:
        json.dump(users, file)

# Function to create a new account
def create_account(username, password):
    users = load_users()
    
    if username in users:
        print("Username already exists.")
        return
    
    users[username] = {"password": password, "wallet": 0}
    save_users(users)
    print("Account created successfully.")

# Function to authenticate a user
def authenticate(username, password):
    users = load_users()
    
    if username in users and users[username]["password"] == password:
        print("Authentication successful.")
        return True
    else:
        print("Invalid username or password.")
        return False

# Function to get user's wallet balance
def get_wallet_balance(username):
    users = load_users()
    return users[username]["wallet"]

# Main program
if __name__ == "__main__":
    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Quit")
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
            break
        else:
            print("Invalid choice. Please try again.")
