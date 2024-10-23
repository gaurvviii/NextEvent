from wallets import create_wallet, send_transaction
from blockchain import connect_to_blockchain

# Connect to the blockchain
web3 = connect_to_blockchain()

# Function to handle payment processing
def handle_payment():
    # List of available payment methods
    payment_methods = ['crypto', 'upi', 'paytm', 'amazon_pay', 'google_pay', 'credit_card', 'debit_card']

    # Prompt user to choose a payment method
    print("Choose a payment method:")
    for i, method in enumerate(payment_methods, 1):
        print(f"{i}. {method}")

    # Get user's choice
    choice = int(input("Enter the number of your payment method: "))

    # Validate choice
    if choice < 1 or choice > len(payment_methods):
        print("Invalid choice. Please try again.")
        return

    payment_method = payment_methods[choice - 1]  # Selected payment method
    amount = float(input("Enter the amount to pay: "))  # Get amount

    if payment_method == 'crypto':
        private_key = input("Enter your crypto wallet private key: ")
        receiver_address = input("Enter the receiver's wallet address: ")

        # Send crypto payment
        tx_hash = send_transaction(private_key, receiver_address, amount)
        print(f"Crypto transaction successful with hash: {tx_hash}")

    else:
        # Simulate traditional payment processing
        print(f"Redirecting to {payment_method} payment portal...")
        # Simulate success message after redirection
        print(f"{payment_method} payment successful!")

# Example usage
if __name__ == '__main__':
    handle_payment()


