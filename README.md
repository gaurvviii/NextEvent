# NextEvent - Decentralized Event Ticketing Platform

## Overview

**NextEvent** is a decentralized event ticketing platform that leverages blockchain technology for secure transactions. It provides flexible payment options including UPI, Paytm, Google Pay, credit/debit cards, and cryptocurrency. The platform allows users to enjoy features such as PayLater, peer-to-peer ticket reselling, and a loyalty rewards system for returning or exchanging tickets.

## Key Features

- **Blockchain Integration**: Ensures secure transactions using decentralized technology.
- **Cryptocurrency Payments**: Supports crypto transactions in addition to conventional payment methods.
- **PayLater Option**: Offers flexibility for users to book now and pay later.
- **Loyalty & Rewards System**: Earn loyalty coins for returning tickets within 5 minutes of the show starting, or for repeat purchases.
- **Peer-to-Peer Ticket Reselling**: A secure portal for users to resell their tickets directly to other buyers.
- **Personalized Recommendations**: Offers event recommendations based on user preferences and past behavior.
  
## Tech Stack

- **Backend**: Python, Blockchain (Ganache, Web3), Flask
- **Payments**: UPI, Paytm, Google Pay, Cryptocurrency integration
- **Frontend**: Streamlit (for demo purposes)
- **Database**: CSV-based data handling (events.csv)

## Getting Started

### Prerequisites
- Python 3.x
- Ganache (for blockchain simulation)
- React.js
- Tailwind CSS

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/nextevent.git
    ```

2. Set up a virtual environment:
    ```bash
    cd nextevent
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    streamlit run streamlitapp.py
    ```

## Usage

1. Choose an event to book tickets, pay using the preferred method (UPI, crypto, etc.).
2. Return tickets within 5 minutes of the show start to earn loyalty coins.
3. Use loyalty coins for discounts on future tickets or other rewards.

## Challenges

- **Compatibility Issues**: Encountered issues with dependencies such as NumPy compatibility and module imports. These were resolved by downgrading/compiling specific versions and restructuring the backend code.
- **Blockchain Integration**: Developing secure, user-friendly blockchain interactions for payments and transactions.

## Future Enhancements

- Integration of live event data using APIs.
- Expansion of payment options for a wider global audience.
- AI-based enhanced recommendation system.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

