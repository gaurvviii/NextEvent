from web3 import Web3
from eth_account import Account

# Connect to local Ethereum node (Ganache)
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connection is successful
if web3.is_connected():
    print("Connected to Ganache!")
else:
    print("Connection failed.")

# Create a new wallet (private key and address)
def create_wallet():
    account = Account.create()
    private_key = account.key.hex()
    wallet_address = account.address
    return private_key, wallet_address

# Function to send a transaction
def send_transaction(sender_private_key, receiver_address, amount):
    sender_account = Account.from_key(sender_private_key)

    # Get the current nonce (transaction count) of the sender
    nonce = web3.eth.get_transaction_count(sender_account.address)

    # Build the transaction with a lower gas price (e.g., 10 Gwei)
    transaction = {
        'nonce': nonce,
        'to': receiver_address,
        'value': web3.to_wei(amount, 'ether'),  # Amount to send in Ether
        'gas': 2000000,  # Set gas limit (arbitrary high value)
        'gasPrice': web3.to_wei('10', 'gwei')  # Set lower gas price
    }

    # Sign the transaction with the sender's private key
    signed_tx = web3.eth.account.sign_transaction(transaction, sender_private_key)

    # Send the transaction and get the transaction hash
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return web3.to_hex(tx_hash)

# Function to check the status of a transaction
def check_transaction_status(tx_hash):
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    if receipt:
        print("Transaction confirmed!")
    else:
        print("Transaction pending...")

# Main function to handle user inputs
def main():
    print("\n--- Wallet and Transaction Management ---\n")
    
    # Ask user if they want to create a new wallet
    create_wallet_choice = input("Do you want to create a new wallet? (yes/no): ").strip().lower()
    if create_wallet_choice == 'yes':
        private_key, wallet_address = create_wallet()
        print(f"New wallet created:\nAddress: {wallet_address}\nPrivate Key: {private_key}")
    
    # Ask user if they want to send a transaction
    send_tx_choice = input("\nDo you want to send a transaction? (yes/no): ").strip().lower()
    if send_tx_choice == 'yes':
        # Get the details from the user
        sender_private_key = input("Enter your private key: ").strip()
        receiver_address = input("Enter the recipient's address: ").strip()
        amount = float(input("Enter the amount of Ether to send: ").strip())
        
        # Send the transaction
        try:
            tx_hash = send_transaction(sender_private_key, receiver_address, amount)
            print(f"Transaction successful with hash: {tx_hash}")
            
            # Check the status of the transaction
            check_tx_choice = input("Do you want to check the transaction status? (yes/no): ").strip().lower()
            if check_tx_choice == 'yes':
                check_transaction_status(tx_hash)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

