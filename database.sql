create database Bank;
use Bank;
create table Customer(Cellphone_num varchar(15) primary key, first_name varchar(20), middle_name varchar(20) default ' ', last_name varchar(20), ID_num INT, Password varchar(100), status INT default 1);
create table Account(Card_num char(16) primary key, Shaba_num varchar(30), amount INT, SATNA INT, PAYA INT, card_to_card INT, owner varchar(15), FOREIGN KEY(owner) references Customer(Cellphone_num));
create table transaction_types(id INT primary key , type varchar(30));
create table Transaction(transaction_id INT AUTO_INCREMENT primary key, sender CHAR(16), receiver CHAR(16), type INT, time DATETIME, amount INT, foreign key(sender) references Account(Card_num), foreign key (receiver) references Account(Card_num), foreign key(type) references transaction_types(id));
insert into transaction_types values (0, 'card_to_card'), (1, 'PAYA'), (2, 'SATNA');

-- trigger
DELIMITER //

CREATE TRIGGER after_insert_transaction
AFTER INSERT ON Transaction FOR EACH ROW
BEGIN
    UPDATE Account
    SET amount = amount - NEW.amount
    WHERE Card_num = NEW.sender;
    UPDATE Account
    SET amount = amount + NEW.amount
    WHERE Card_num = NEW.receiver;
    CASE NEW.type
        WHEN 0 THEN
            UPDATE Account
            SET card_to_card = card_to_card + NEW.amount
            WHERE Card_num = NEW.sender;
        WHEN 1 THEN
            UPDATE Account
            SET SATNA = SATNA + NEW.amount
            WHERE Card_num = NEW.sender;
        WHEN 2 THEN
            UPDATE Account
            SET PAYA = PAYA + NEW.amount
            WHERE Card_num = NEW.sender;
    END CASE;
END;
//

DELIMITER ;
