from body import *


def main_menu():
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
    print("4. Transaction validation")
    print("5. view your accounts")
    print("6. logout")
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
        user_menu_loop(cellphone_num)
        return 1
    else:
        return 0


def login_menu():
    clear_screen()
    print("Login Form")
    cellphone_num = input("Cellphone Number: ")
    password = input("Password: ")
    result = login(cellphone_num, password)
    if result:
        user_menu_loop(cellphone_num)
        return 1
    else:
        return 0

def create_account_menu(cellphone_num):
    clear_screen()
    print("Create Account Form")
    amount = int(input("Initial Amount: "))
    create_account(cellphone_num, amount)
    input("Press Enter to continue...")


def make_transaction_menu(cellphone_num):
    clear_screen()
    accounts = session.query(Account).filter_by(owner=cellphone_num)
    count = 0
    clear_screen()
    accs = []
    for i in accounts:
        acc_card_num = i.Card_num
        accs.append((count, acc_card_num))
        count += 1
    clear_screen()
    for i in accs:
        print(f"{i[0]}: {i[1]}")
    sender = input("Choose Account: ")
    sender = accs[int(sender)][1]
    clear_screen()
    receiver = input("Receiver Card Number: ")
    clear_screen()
    print("Make Transaction Form")
    amount = int(input("Amount: "))
    clear_screen()
    type_ = int(input("Transaction Type (0 for card-to-card, 1 for SATNA, 2 for PAYA): "))
    transfer(sender, receiver, amount, type_)
    input("Press Enter to continue...")


def view_last_n_transactions_menu(cellphone_num):
    accounts = session.query(Account).filter_by(owner=cellphone_num)
    clear_screen()
    print("View Last N Transactions Form")
    count = 0
    accs = []
    for i in accounts:
        acc_card_num = i.Card_num
        accs.append((count, acc_card_num))
        count += 1
    clear_screen()
    for i in accs:
        print(f"{i[0]}: {i[1]}")
    acc = input("Choose Account: ")
    acc = accs[int(acc)][1]
    clear_screen()
    n = int(input("Enter N: "))
    last_n(acc, n)
    input("Press Enter to continue...")


def transaction_validation_menu(cellphone_num):
    clear_screen()
    transactionid = input("Enter transaction id:")
    transaction_validation(transactionid, cellphone_num)
    input("Press Enter to continue...")


def view_accounts_menu(cellphone_num):
    accounts = session.query(Account).filter_by(owner=cellphone_num)
    count = 0
    accs = []
    for i in accounts:
        acc_card_num = i.Card_num
        acc_shaba = i.Shaba_num
        acc_amount = i.amount
        acc_c2climit = i.card_to_card
        acc_satnalimit = i.SATNA
        acc_payalimit = i.PAYA
        accs.append((count, acc_card_num, acc_shaba, acc_amount, acc_c2climit, acc_satnalimit, acc_payalimit))
        count += 1
    clear_screen()
    for i in accs:
        print(f'{i[0]}: card_num-> {i[1]} , shaba_num-> {i[2]} , amount->{i[3]} , today card to card->{i[4]} , today SATNA->{i[5]} , today PAYA->{i[6]}')
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
            transaction_validation_menu(cellphone_num)
        elif choice == '5':
            view_accounts_menu(cellphone_num)
        elif choice == '6':
            break


def main():
    result = 1
    while True:
        clear_screen()
        if not result:
            print('An error occurred try again!\n')
        choice = main_menu()
        if choice == '1':
            result = sign_up()
        elif choice == '2':
            result = login_menu()
        elif choice == '3':
            break


if __name__ == "__main__":
    main()
    session.close()
