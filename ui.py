from body import *


def main_menu():
    clear_screen()
    print("Welcome to the Bank!")
    print("1. Sign-up")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice


def user_menu():
    clear_screen()
    print("1. Create Account")
    print("2. Make Transaction")
    print("3. View Last N Transactions")
    print("4. Logout")
    choice = input("Enter your choice: ")
    return choice


def sign_up():
    clear_screen()
    print("Sign-up Form")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    ID_num = input("ID Number: ")
    cellphone_num = input("Cellphone Number: ")
    password = input("Password: ")
    result = signup(first_name, last_name, ID_num, cellphone_num, password)
    if result:
        input("Press Enter to continue...")


def login_menu():
    clear_screen()
    print("Login Form")
    cellphone_num = input("Cellphone Number: ")
    password = input("Password: ")
    result = login(cellphone_num, password)
    if result:
        user_menu_loop(cellphone_num)


def create_account_menu(cellphone_num):
    clear_screen()
    print("Create Account Form")
    amount = int(input("Initial Amount: "))
    create_account(cellphone_num, amount)
    input("Press Enter to continue...")


def make_transaction_menu(cellphone_num):
    clear_screen()
    print("Make Transaction Form")
    sender = input("Sender Card Number: ")
    receiver = input("Receiver Card Number: ")
    amount = int(input("Amount: "))
    type_ = int(input("Transaction Type (0 for card-to-card, 1 for SATNA, 2 for PAYA): "))
    transfer(sender, receiver, amount, type_)
    input("Press Enter to continue...")


def view_last_n_transactions_menu(cellphone_num):
    clear_screen()
    print("View Last N Transactions Form")
    card_num_ = input("Enter Card Number: ")
    n = int(input("Enter N: "))
    last_n(card_num_, n)
    input("Press Enter to continue...")


def user_menu_loop(cellphone_num):
    while True:
        choice = user_menu()
        if choice == '1':
            create_account_menu(cellphone_num)
        elif choice == '2':
            make_transaction_menu(cellphone_num)
        elif choice == '3':
            view_last_n_transactions_menu(cellphone_num)
        elif choice == '4':
            break


def main():
    while True:
        choice = main_menu()
        if choice == '1':
            sign_up()
        elif choice == '2':
            login_menu()
        elif choice == '3':
            break


if __name__ == "__main__":
    main()
    session.close()
