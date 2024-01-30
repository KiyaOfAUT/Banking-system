from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, desc, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from hashlib import sha256
import os
import random
from datetime import datetime


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


engine = create_engine('mysql://root:*xV75pc92hI2@localhost/Bank', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

mil = 1000000
transaction_type = [10 * mil, 100 * mil, 200 * mil]

class Customer(Base):
    __tablename__ = 'Customer'

    Cellphone_num = Column(String(15), primary_key=True)
    first_name = Column(String(20))
    middle_name = Column(String(20), default=' ')
    last_name = Column(String(20))
    ID_num = Column(Integer)
    Password = Column(String(100))
    status = Column(Integer, default=1)


class Account(Base):
    __tablename__ = 'Account'

    Card_num = Column(String(16), primary_key=True)
    Shaba_num = Column(String(30))
    amount = Column(Integer)
    SATNA = Column(Integer)
    PAYA = Column(Integer)
    card_to_card = Column(Integer)
    owner = Column(String(15), ForeignKey('Customer.Cellphone_num'))


class TransactionType(Base):
    __tablename__ = 'transaction_types'

    id = Column(Integer, primary_key=True)
    type = Column(String(30))


class Transaction(Base):
    __tablename__ = 'Transaction'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(String(16), ForeignKey('Account.Card_num'))
    receiver = Column(String(16), ForeignKey('Account.Card_num'))
    type = Column(Integer, ForeignKey('transaction_types.id'))
    time = Column(DateTime)
    amount = Column(Integer)



def generate_random_card_number():
    card_num = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    card_num = '61231258' + card_num
    last_digit = 0
    for i in range(15):
        last_digit += int(card_num[i]) * 2
        i += 1
        if i < 15:
            last_digit += int(card_num[i])
        i += 1
    last_digit = 10 - (last_digit % 10)
    card_num += str(last_digit)
    return card_num


def is_card_number_unique(card_number):
    return session.query(Account).filter_by(Card_num=card_number).first() is None


def shaba(card_num):
    return 'IR06082000' + card_num


def create_account(cellphone_num, amount):
    try:
        card_number = generate_random_card_number()
        while not is_card_number_unique(card_number):
            card_number = generate_random_card_number()
        shaba_num = shaba(card_number)
        new_account = Account(
            Card_num=card_number,
            Shaba_num=shaba_num,
            amount=amount,
            SATNA=0,
            PAYA=0,
            card_to_card=0,
            owner=cellphone_num
        )
        session.add(new_account)
        session.commit()
        clear_screen()
        print(f"Account created successfully.\n Card number: {card_number} \n shaba number: {shaba_num}")

    except Exception as e:
        session.rollback()
        clear_screen()
        print(f"Account creation failed. An unexpected error occurred: {e}")


def signup(first_name, last_name, ID_num, cellphone_num, password, middle_name=''):
    try:
        hashed_password = sha256(password.encode()).hexdigest()
        new_customer = Customer(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            ID_num=ID_num,
            Cellphone_num=cellphone_num,
            Password=hashed_password
        )
        session.add(new_customer)
        session.commit()
        clear_screen()
        print(f"signup successful!\n welcome to our bank {first_name} {last_name}")
        return 1

    except IntegrityError as e:
        session.rollback()  # Rollback the transaction to prevent partial changes
        error_info = e.orig.args
        clear_screen()
        if "Duplicate entry" in error_info[1]:
            print(f"Sign-up failed. User with cellphone number {cellphone_num} already exists.")
        else:
            print(f"Sign-up failed. An unexpected error occurred: {error_info}")
        return 0

    except Exception as e:
        session.rollback()
        clear_screen()
        print(f"Sign-up failed. An unexpected error occurred: {e}")
        return 0


def login(cellphone_num, password):
    hashed_password = sha256(password.encode()).hexdigest()
    user = session.query(Customer).filter_by(Cellphone_num=cellphone_num, Password=hashed_password).first()
    clear_screen()
    if user:
        return user.Cellphone_num
    else:
        return 0


def card_num(num):
    if num[:10] == 'IR06082000':
        return num[-16:]
    else:
        return num


def card_to_card(sender, receiver, amount):
    try:
        account = session.query(Account).filter_by(Card_num=sender).first()
        rcv = session.query(Account).filter_by(Card_num=receiver).first()
        if not rcv:
            clear_screen()
            print(f"wrong receiver!\nno account with number {receiver} found!")
            return 0
        if amount <= account.amount:
            if account.card_to_card + amount < transaction_type[0]:
                new_transaction = Transaction(sender=sender, receiver=receiver, type=0, time=datetime.now(), amount=amount)
                session.add(new_transaction)
                session.commit()
                transactionid = new_transaction.transaction_id
                clear_screen()
                print(f"successfully transferred! \n your transaction id : {transactionid}")
            else:
                session.rollback()
                clear_screen()
                print('requested amount exceeds daily limit!!')
                return 0
        else:
            session.rollback()
            clear_screen()
            print('not enough money in your account!!')
            return 0
    except Exception as e:
        session.rollback()
        clear_screen()
        print(f"Sign-up failed. An unexpected error occurred: {e}")
        return 0


def paya(sender, receiver, amount):
    try:
        account = session.query(Account).filter_by(Card_num=sender).first()
        if amount <= account.amount:
            if account.PAYA + amount < transaction_type[1]:
                new_transaction = Transaction(sender=sender, receiver=receiver, type=1, time=datetime.now(), amount=amount)
                session.add(new_transaction)
                session.commit()
                transactionid = new_transaction.transaction_id
                clear_screen()
                print(f"successfully transferred! \n your transaction id : {transactionid}")
            else:
                session.rollback()
                clear_screen()
                print('requested amount exceeds daily limit!!')
                return 0
        else:
            session.rollback()
            clear_screen()
            print('not enough money in your account!!')
            return 0
    except Exception as e:
        session.rollback()
        clear_screen()
        print(f"Sign-up failed. An unexpected error occurred: {e}")
        return 0


def satna(sender, receiver, amount):
    try:
        account = session.query(Account).filter_by(Card_num=sender).first()
        if amount <= account.amount:
            if account.SATNA + amount < transaction_type[2]:
                new_transaction = Transaction(sender=sender, receiver=receiver, type=2, time=datetime.now(), amount=amount)
                session.add(new_transaction)
                session.commit()
                transactionid = new_transaction.transaction_id
                clear_screen()
                print(f"successfully transferred! \n your transaction id : {transactionid}")
            else:
                session.rollback()
                clear_screen()
                print('requested amount exceeds daily limit!!')
                return 0
        else:
            session.rollback()
            clear_screen()
            print('not enough money in your account!!')
            return 0
    except Exception as e:
        session.rollback()
        clear_screen()
        print(f"Sign-up failed. An unexpected error occurred: {e}")
        return 0


def transfer(sender, receiver, amount, type_):
    sender = card_num(sender)
    receiver = card_num(receiver)
    if type_ < 0 or type_ > 2 or amount < 0 or not sender or not receiver:
        clear_screen()
        print("wrong input!")
        return 0
    if type_ == 0:
        return card_to_card(sender, receiver, amount)
    elif type_ == 1:
        return satna(sender, receiver, amount)
    else:
        return paya(sender, receiver, amount)


def transaction_validation(transactionid, cell_num):
    user_accounts = session.query(Account).filter_by(owner=cell_num).all()
    for i in user_accounts:
        transaction = session.query(Transaction).filter_by(transaction_id=transactionid).first()
        if transaction:
            if i.Card_num == transaction.sender or i.Card_num == transaction.receiver:
                clear_screen()
                print(f"transaction is valid!\n {transaction.amount} is transferred from {transaction.sender} to {transaction.receiver}\n")
                return 1
    clear_screen()
    print("no transaction was found!")
    return 0


def last_n(card_num_, n):
    card_num_ = card_num(card_num_)
    transactions = (
        session.query(Transaction)
        .filter(or_(Transaction.sender == card_num_, Transaction.receiver == card_num_))
        .order_by(desc(Transaction.time))
        .limit(n)
        .all()
    )
    clear_screen()
    if transactions:
        for i in transactions:
            if i.sender == card_num_:
                print(f"sent {i.amount} to {i.receiver} at {i.time}")
            else:
                print(f"received {i.amount} from {i.sender} at {i.time}")
    else:
        print("no recent transaction!\n")

