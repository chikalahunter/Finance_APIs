from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from models import save_users, load_users

app = FastAPI()


# Model for representing a transaction
class Transaction(BaseModel):
    username: str
    amount: float

# Function to retrieve all transactions for a user
def get_user_transactions(username: str):
    transactions = []
    return transactions

def authenticate():
    authenticated_user = "authenticated_user"  
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Unauthorized: User not authenticated")
    return authenticated_user


# Endpoint to retrieve all transactions for a user
@app.get("/transactions/{username}", response_model=List[Transaction])
def retrieve_transactions(username: str, current_user: str = Depends(authenticate)):
    if username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own transactions.")
    
    transactions = get_user_transactions(username)
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found.")
    
    return transactions

# Model for representing a funding request
class FundRequest(BaseModel):
    username: str
    amount: float

# Function to create a transaction and update the user's wallet balance
def create_transaction(username: str, amount: float):
    users = load_users()

    if username in users:
        if amount > 0:
            users[username]["wallet"] += amount
            save_users(users)
        else:
            raise HTTPException(status_code=400, detail="Invalid transaction amount. Please enter a positive value.")
    else:
        raise HTTPException(status_code=404, detail="User not found. Please create an account.")

# Function to fund the user's account
def fund_account(request: FundRequest, current_user: str = Depends(authenticate)):
    if request.username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only fund your own account.")
    
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid funding amount. Please enter a positive value.")
    

    
    # Update the user's wallet balance with the specified amount
    create_transaction(request.username, request.amount)
    
    return {"message": "Funds successfully added to your account."}

# Endpoint to allow users to fund their account
@app.post("/fund-account", response_model=dict)
def fund_user_account(request: FundRequest, current_user: str = Depends(authenticate)):
    return fund_account(request, current_user)


# Model for representing a wallet response
class WalletResponse(BaseModel):
    username: str
    balance: float


# Function to get user's wallet balance
def get_wallet_balance(username: str, current_user: str = Depends(authenticate)):
    if username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own wallet balance.")
    
    balance = 0  
    
    return WalletResponse(username=username, balance=balance)

# Endpoint to allow users to retrieve their wallet balance
@app.get("/wallet/{username}", response_model=WalletResponse)
def retrieve_wallet_balance(username: str, current_user: str = Depends(authenticate)):
    return get_wallet_balance(username, current_user)

# Model for representing a money transfer request
class TransferRequest(BaseModel):
    sender_username: str
    recipient_username: str
    amount: float


# Function to transfer money from sender to recipient
def transfer_money(request: TransferRequest, current_user: str = Depends(authenticate)):
    if request.sender_username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only initiate transfers from your own wallet.")

    # Check if the sender has enough funds
    sender_balance = get_wallet_balance(request.sender_username)
    if sender_balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds for the transfer.")

    # Deduct the amount from the sender's wallet
    create_transaction(request.sender_username, -request.amount)

    # Add the amount to the recipient's wallet
    create_transaction(request.recipient_username, request.amount)

    return {"message": "Money transfer successful."}

# Endpoint to initiate a money transfer
@app.post("/transfer-money", response_model=dict)
def initiate_transfer(request: TransferRequest, current_user: str = Depends(authenticate)):
    return transfer_money(request, current_user)


# Model for representing a bank transfer request
class BankTransferRequest(BaseModel):
    sender_username: str
    bank_account_number: str
    amount: float


# Function to transfer money to a bank account
def transfer_to_bank_account(request: BankTransferRequest, current_user: str = Depends(authenticate)):
    if request.sender_username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only initiate bank transfers from your own wallet.")

    # Check if the sender has enough funds
    sender_balance = get_wallet_balance(request.sender_username)
    if sender_balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds for the bank transfer.")

 # Deduct the amount from the sender's wallet
    create_transaction(request.sender_username, -request.amount)

    # Record the bank transfer details 
    transfer_details = {
        "sender": request.sender_username,
        "recipient_account": request.bank_account_number,
        "amount": request.amount,
        "status": "Completed"  
    }


    return {"message": "Bank transfer initiated successfully.", "transfer_details": dict(transfer_details)}


# Endpoint to initiate a bank transfer
@app.post("/transfer-to-bank-account", response_model=dict)
def initiate_bank_transfer(request: BankTransferRequest, current_user: str = Depends(authenticate)):
    return transfer_to_bank_account(request, current_user)


# Model for representing a beneficiary bank account
class BeneficiaryAccount(BaseModel):
    username: str
    beneficiary_name: str
    beneficiary_account_number: str
  
def add_beneficiary_account(account: BeneficiaryAccount, current_user: str = Depends(authenticate)):
    if account.username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only add beneficiaries to your own account.")
    return {"message": "Beneficiary bank account added successfully."}

# Endpoint to allow users to add beneficiary bank accounts
@app.post("/add-beneficiary", response_model=dict)
def add_beneficiary(account: BeneficiaryAccount, current_user: str = Depends(authenticate)):
    return add_beneficiary_account(account, current_user)
    
# Model for representing a beneficiary bank account
class BeneficiaryAccount(BaseModel):
    beneficiary_name: str
    beneficiary_account_number: str

# Function to retrieve beneficiary bank accounts
def get_beneficiary_accounts(username: str, current_user: str = Depends(authenticate)):
    if username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only retrieve beneficiaries for your own account.")
    
    beneficiary_accounts = []

    return beneficiary_accounts

# Endpoint to allow users to retrieve beneficiary bank accounts
@app.get("/beneficiary-accounts", response_model=List[BeneficiaryAccount])
def retrieve_beneficiary_accounts(current_user: str = Depends(authenticate)):
    return get_beneficiary_accounts(current_user, current_user)

# Model for representing an airtime purchase request
class AirtimePurchaseRequest(BaseModel):
    sender_username: str
    recipient_phone_number: str
    network: str
    amount: float

# Model for representing beneficiary phone numbers
class BeneficiaryPhoneNumber(BaseModel):
    username: str
    phone_number: str

# Function to buy airtime for a specific network and phone number
def buy_airtime(request: AirtimePurchaseRequest, current_user: str = Depends(authenticate)):
    if request.sender_username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only buy airtime from your own wallet.")

    # Check if the sender has enough funds
    sender_balance = get_wallet_balance(request.sender_username)
    if sender_balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds for the airtime purchase.")

 # Deduct the amount from the sender's wallet
    create_transaction(request.sender_username, -request.amount)

    return {"message": f"Airtime purchased successfully for {request.network} network."}

# Function to add beneficiary phone numbers
def add_beneficiary_phone_number(phone_number: BeneficiaryPhoneNumber, current_user: str = Depends(authenticate)):
    if phone_number.username != current_user:
        raise HTTPException(status_code=403, detail="Forbidden: You can only add beneficiaries to your own account.")

    return {"message": f"Beneficiary phone number {phone_number.phone_number} added successfully."}

# Endpoint to initiate an airtime purchase
@app.post("/buy-airtime", response_model=dict)
def initiate_airtime_purchase(request: AirtimePurchaseRequest, current_user: str = Depends(authenticate)):
    return buy_airtime(request, current_user)

# Endpoint to add beneficiary phone numbers
@app.post("/add-beneficiary-phone", response_model=dict)
def add_beneficiary(request: BeneficiaryPhoneNumber, current_user: str = Depends(authenticate)):
    return add_beneficiary_phone_number(request, current_user)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



