import streamlit as st
import base64
import random

def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

background_image_base64 = get_image_as_base64("background.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{background_image_base64}");
        background-size: cover;
        background-position: center;
    }}
    .reportview-container .main .block-container{{
        padding-top: 5rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 5rem;
    }}
    .fixed-bottom {{
        position: fixed;
        right: 1rem;
        bottom: 1rem;
        width: auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Parent Class
class User:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def show_details(self):
        st.write('Personal Details:')
        st.write('Name: ', self.name)
        st.write('Gender: ', self.gender)
        st.write('Age: ', self.age)
balance_placeholder = st.empty()
# Child Class
class Bank(User):
    def __init__(self, name, gender, age):
        super().__init__(name, gender, age)
        self.balance = 0

    def deposit(self, amount):
        self.amount = amount
        self.balance += self.amount
        st.session_state['balance'] = self.balance

    def withdrawal(self, amount):
        self.amount = amount
        if self.amount > self.balance:
            pass
        else:
            self.balance -= self.amount
            st.session_state['balance'] = self.balance

    def view_balance(self):
        self.show_details()
        st.write('The available balance is $', self.balance)

class Credentials:
    def __init__(self):
        self.username = "Muzammil"
        self.password = "NUST"

    def verify_credentials(self, input_username, input_password):
        return input_username == self.username and input_password == self.password

# Function to check login credentials
def check_login(username: str, password: str) -> bool:
    creds = Credentials()
    return creds.verify_credentials(username, password)

def deposit_callback():
    amount = st.session_state.amount_to_deposit
    user_bank.deposit(amount)
    st.success(f"Deposited \${amount:.2f}. Your new balance is \${user_bank.balance:.2f}")
    st.experimental_rerun()

def withdrawal_callback():
    amount = st.session_state.amount_to_withdraw
    user_bank.withdrawal(amount)
    if amount <= user_bank.balance:
        st.success(f"Withdrew \${amount:.2f}. Your new balance is \${user_bank.balance:.2f}")
    else:
        st.error('Insufficient Funds.')
    st.experimental_rerun()

def handle_bank_operations(user_bank):
    action = st.selectbox("Choose an action", ["Deposit", "Withdraw"])
    
    if action == "Deposit":
        amount = st.number_input("Amount to deposit", min_value=0.01, key='amount_to_deposit')
        if st.button("Deposit"):
            user_bank.deposit(amount)
            balance_placeholder.markdown(f"#### Your available balance is ${st.session_state['balance']:,.2f}")
            st.success(f"Deposited \${amount:.2f}. Your new balance is \${user_bank.balance:.2f}")

    elif action == "Withdraw":
        amount = st.number_input("Amount to withdraw", min_value=0.01, key='amount_to_withdraw')
        if st.button("Withdraw"):
            user_bank.withdrawal(amount)
            if amount > user_bank.balance:
                st.error('Insufficient Funds. The available balance is ${:.2f}'.format(user_bank.balance))
            else:
                balance_placeholder.markdown(f"#### Your available balance is ${st.session_state['balance']:,.2f}")
                st.success(f"Withdrew \${amount:.2f}. Your new balance is \${user_bank.balance:.2f}")

# Streamlit code for the login interface
def login_ui():
    st.title("Habib Bank Limited - Online Banking")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_login(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
        else:
            st.error("Invalid username or password.")

# Initialize session state for login status and user details
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# Main app logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

if not st.session_state.get('logged_in', False):
    login_ui()
else:
    st.title(f"Welcome, {st.session_state['username']}!")
    
    # Create a placeholder for the balance at the top of the page
    balance_placeholder = st.empty()

    # Initially set the balance placeholder with the current balance
    if 'balance' not in st.session_state or st.session_state['balance'] is None:
        st.session_state['balance'] = random.uniform(1, 10000)
    balance_placeholder.markdown(f"#### Your available balance is ${st.session_state['balance']:,.2f}")

    user_bank = Bank(st.session_state['username'], "Gender", 30)
    user_bank.balance = st.session_state['balance']
    handle_bank_operations(user_bank)

    if st.button('Logout', key='logout'):
        st.session_state.clear()
        st.experimental_rerun()

    st.markdown('<div class="fixed-bottom"></div>', unsafe_allow_html=True)