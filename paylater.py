import pandas as pd

# Load the dataset
data = pd.read_csv('events.csv')

# Function to check PayLater option and balance
def check_pay_later(user_id, event_id, amount_to_pay):
    user_data = data[(data['user_id'] == user_id) & (data['event_id'] == event_id)]
    
    if not user_data.empty:
        wallet_balance = user_data['wallet_balance'].values[0]
        pay_later_option = user_data['pay_later'].values[0]

        if pay_later_option and wallet_balance < amount_to_pay:
            print("PayLater option can be used.")
            return "paylater"
        elif wallet_balance >= amount_to_pay:
            print("You can proceed with the payment from your wallet.")
            return "wallet"
        else:
            print("Insufficient funds and PayLater option not available.")
            return "insufficient"
    else:
        return "Event not found."

# Function to handle payment method
def process_payment(payment_method, amount_to_pay):
    if payment_method == 'bank':
        account_number = input("Enter your bank account number: ")
        bank_name = input("Enter your bank name: ")
        print(f"Processing payment of {amount_to_pay} through bank account {account_number} at {bank_name}.")

    elif payment_method == 'crypto':
        wallet_address = input("Enter your crypto wallet address: ")
        print(f"Processing crypto payment of {amount_to_pay} to wallet {wallet_address}.")

    elif payment_method == 'paylater':
        print("Choose one of the PayLater options:")
        print("1. Klarna")
        print("2. Afterpay")
        print("3. Affirm")
        paylater_choice = input("Select a PayLater service (1/2/3): ")

        if paylater_choice == '1':
            print(f"Processing {amount_to_pay} payment with Klarna.")
        elif paylater_choice == '2':
            print(f"Processing {amount_to_pay} payment with Afterpay.")
        elif paylater_choice == '3':
            print(f"Processing {amount_to_pay} payment with Affirm.")
        else:
            print("Invalid choice.")

# Function to handle installment payments
def process_installments(total_amount, num_installments):
    installment_amount = total_amount / num_installments
    print(f"You have chosen {num_installments} installments. Each installment will be: {installment_amount:.2f}")

# Example usage
user_id = 101
event_id = 1
amount_to_pay = 100

# Check if the user can use PayLater or proceed with wallet payment
payment_option = check_pay_later(user_id, event_id, amount_to_pay)

if payment_option == "paylater":
    num_installments = int(input("Enter the number of installments (e.g., 3, 6, 12): "))
    process_installments(amount_to_pay, num_installments)
    
    payment_method = input("Enter payment method (bank/crypto/paylater): ").lower()
    process_payment(payment_method, amount_to_pay)

elif payment_option == "wallet":
    payment_method = input("Enter payment method (bank/crypto/wallet): ").lower()
    process_payment(payment_method, amount_to_pay)

elif payment_option == "insufficient":
    print("No sufficient balance, and PayLater option is not available for this event.")

