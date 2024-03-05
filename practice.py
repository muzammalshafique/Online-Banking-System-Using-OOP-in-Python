import streamlit as st
import base64
import random

# Function to get base64 string of the image for background
def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# CSS to set a background image
# Replace 'background.jpg' with your actual image file name
background_image_base64 = get_image_as_base64("background.jpg") # Ensure the file is in the same directory
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
    /* This CSS is for logout button to be at the bottom right */
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
class User():
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def show_details(self):
        st.write('Personal Details:')
        st.write('Name: ', self.name)
        st.write('Gender: ', self.gender)
        st.write('Age: ', self.age)

# Child Class
class Bank(User):
    def __init__(self, name, gender, age):
        super().__init__(name, gender, age)
        self.balance = 0

    def deposit(self, amount):
        self.amount = amount
        self.balance += self.amount
        st.session_state['balance'] = self.balance
        # st.write('Account Balance is $', self.balance)

    def withdrawal(self, amount):
        self.amount = amount
        if self.amount > self.balance:
            st.error('Insufficient Funds. The available balance is ${:.2f}'.format(self.balance))
        else:
            self.balance -= self.amount
            st.session_state['balance'] = self.balance
            # st.write('Remaining Balance is $', self.balance)

    def view_balance(self):
        self.show_details()
        st.write('The available balance is $', self.balance)

class Credentials:
        def __init__(self):
            # Storing the credentials - not secure for a production environment
            self.username = "Muzammil"
            self.password = "NUST"

        def verify_credentials(self, input_username, input_password):
            # Check if the input credentials match the stored credentials
            return input_username == self.username and input_password == self.password

# Function to check login credentials
def check_login(username: str, password: str) -> bool:
    creds = Credentials()
    return creds.verify_credentials(username, password)

def handle_bank_operations(user_bank):
    # Remove the "Check Balance" option from the selectbox
    action = st.selectbox("Choose an action", ["Deposit", "Withdraw"])
    if action == "Deposit":
        amount = st.number_input("Amount to deposit", min_value=0.01)
        if st.button("Deposit"):
            user_bank.deposit(amount)
            st.success(f"Your account has been credited by \${amount:.2f}. Your current balance is \${user_bank.balance:.2f}.")
    elif action == "Withdraw":
        amount = st.number_input("Amount to withdraw", min_value=0.01)
        if st.button("Withdraw"):
            user_bank.withdrawal(amount)
            if amount > user_bank.balance:
                st.error('Insufficient Funds.')
            else:
                st.success(f"Your account has been debited by \${amount:.2f}. Your current balance is \${user_bank.balance:.2f}.")
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
if not st.session_state.get('logged_in', False):
    login_ui()
else:
    st.title(f"Welcome, {st.session_state['username']}!")
    
    # Initialize or update the session state balance
    if 'balance' not in st.session_state or st.session_state['balance'] is None:
        st.session_state['balance'] = random.uniform(1, 10000)  # Generates a random balance

    # Display the session state balance
    st.markdown(f"#### Your available balance is ${st.session_state['balance']:,.2f}")

    # Create a Bank object for the logged-in user with the session state balance
    user_bank = Bank(st.session_state['username'], "Gender", 30)
    user_bank.balance = st.session_state['balance']  # Set the bank balance to the session state balance
    handle_bank_operations(user_bank)

    # Logout button with the fixed position at the bottom right
    # Place this code at the very end of your app logic
    if st.button('Logout', key='logout'):
        # Clear the session state and log the user out
        st.session_state.clear()
        st.experimental_rerun()

    # This placeholder ensures the logout button is rendered correctly
    st.markdown('<div class="fixed-bottom"></div>', unsafe_allow_html=True)