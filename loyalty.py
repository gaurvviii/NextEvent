import pandas as pd
from web3 import Web3
from eth_account import Account
from datetime import datetime

# Load the dataset
data = pd.read_csv('events.csv')

# Connect to Blockchain
def connect_to_blockchain():
    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    
    if web3.is_connected():
        print("Connected to Blockchain!")
    else:
        print("Connection failed.")
    return web3

web3 = connect_to_blockchain()

# 1. Earning Loyalty Points
def earn_loyalty_points(user_id, amount_spent):
    points_per_dollar = 1  # Points earned per dollar
    loyalty_earn_rate = data.loc[data['user_id'] == user_id, 'loyalty_earn_rate'].values[0]
    
    # Calculate the points earned
    points_earned = amount_spent * loyalty_earn_rate
    
    # Update user's loyalty points
    user_data = data.loc[data['user_id'] == user_id]
    current_points = user_data['loyalty_points'].values[0]
    new_total_points = current_points + points_earned
    
    data.loc[data['user_id'] == user_id, 'loyalty_points'] = new_total_points
    return new_total_points

# 2. Redeeming Loyalty Points
def redeem_loyalty_points(user_id, points_to_redeem):
    user_data = data.loc[data['user_id'] == user_id]
    current_points = user_data['loyalty_points'].values[0]
    
    if current_points >= points_to_redeem:
        # Calculate discount based on points
        discount_amount = points_to_redeem
        
        # Update loyalty points
        new_points_balance = current_points - points_to_redeem
        data.loc[data['user_id'] == user_id, 'loyalty_points'] = new_points_balance
        
        return discount_amount, new_points_balance
    else:
        return "Insufficient points", current_points

# 3. Tracking Loyalty Points Balance
def check_loyalty_points(user_id):
    user_data = data.loc[data['user_id'] == user_id]
    current_points = user_data['loyalty_points'].values[0]
    return current_points

# 4. Loyalty Tiers or Levels
def get_loyalty_tier(user_id):
    points = check_loyalty_points(user_id)
    if points > 100:
        return "Gold"
    elif points > 50:
        return "Silver"
    else:
        return "Bronze"

# 5. PayLater Option with Blockchain Payment Integration
def check_pay_later(user_id, event_id, amount_to_pay):
    user_data = data[(data['user_id'] == user_id) & (data['event_id'] == event_id)]
    
    if not user_data.empty:
        wallet_balance = user_data['wallet_balance'].values[0]
        pay_later_option = user_data['pay_later'].values[0]

        if pay_later_option and wallet_balance < amount_to_pay:
            return "PayLater option can be used."
        elif wallet_balance >= amount_to_pay:
            return "You can proceed with the payment."
        else:
            return "Insufficient funds and PayLater option not available."
    else:
        return "Event not found."

# Crypto Payment Integration
def send_transaction(sender_private_key, receiver_address, amount):
    sender_account = Account.from_key(sender_private_key)
    nonce = web3.eth.get_transaction_count(sender_account.address)
    
    transaction = {
        'nonce': nonce,
        'to': receiver_address,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei')
    }
    
    signed_tx = web3.eth.account.sign_transaction(transaction, sender_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    return web3.to_hex(tx_hash)

def process_payment(user_id, amount_to_pay):
    print("Processing payment...")
    payment_method = input("Enter payment method (crypto/paylater): ").lower()
    
    if payment_method == 'crypto':
        private_key = input("Enter your private key: ")
        receiver_address = input("Enter receiver address: ")
        
        # Processing crypto payment
        tx_hash = send_transaction(private_key, receiver_address, amount_to_pay)
        print(f"Transaction successful with hash: {tx_hash}")
        
        # Earn loyalty points on successful crypto transaction
        new_points_balance = earn_loyalty_points(user_id, amount_to_pay)
        print(f"New Loyalty Points Balance: {new_points_balance}")
    
    elif payment_method == 'paylater':
        event_id = int(input("Enter event ID: "))
        result = check_pay_later(user_id, event_id, amount_to_pay)
        
        if result == "PayLater option can be used.":
            installments = int(input("Enter number of installments: "))
            # Implement PayLater logic here
            print(f"PayLater option used. Amount to be paid in {installments} installments.")
            
            # Earn loyalty points after final installment
            new_points_balance = earn_loyalty_points(user_id, amount_to_pay)
            print(f"New Loyalty Points Balance: {new_points_balance}")
        else:
            print(result)

# Example usage
if __name__ == "__main__":
    user_id = 101  # Assume user is logged in
    amount_to_pay = 100  # Example amount to pay for an event
    process_payment(user_id, amount_to_pay)

    # Display Loyalty Tier
    loyalty_tier = get_loyalty_tier(user_id)
    print(f"Your current loyalty tier: {loyalty_tier}")
    
    # Example of redeeming points
    points_to_redeem = 20
    discount, new_balance = redeem_loyalty_points(user_id, points_to_redeem)
    print(f"Discount Applied: {discount}, New Loyalty Points Balance: {new_balance}")
