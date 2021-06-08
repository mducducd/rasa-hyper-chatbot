import mysql.connector

def DataUpdate(cust_name,cust_cmnd,account_number):
    mydb = mysql.connector.connect( host="localhost", user="root",passwd="root", database="rasa_hyper")
    mycursor = mydb.cursor()
    # sql = 'CREATE TABLE customers (name VARCHAR(255), cmnd VARCHAR(255) , account_number VARCHAR(255),balance INT)'
    balance = 10000000;
    # sql = 'CREATE TABLE service (name VARCHAR(255))'
    # INSERT INTO service(name) VALUES("Đăng ký tài khoản");
    # INSERT INTO service(name) VALUES("Xem số dư tài khoản");
    # INSERT INTO service(name) VALUES("Xem khoản vay tối đa");
    # ALTER TABLE service CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
    # sql='INSERT INTO customers (name, cmnd, account_number,balance) VALUES ("{0}","{1}", "{2}","{3}");'.format(cust_name,cust_cmnd,account_number,balance)
    sql = 'DELETE FROM customers;'
    sql = 'create table services(service VARCHAR(255));' \
          'INSERT INTO services(service) VALUES("Đăng ký tài khoản");' \
          'INSERT INTO services(service) VALUES("Xem số dư tài khoản");' \
          'INSERT INTO services(service) VALUES("Xem số dư tài khoản");' \
          'INSERT INTO services(service) VALUES("Chuyển khoản");' \
          'CREATE TABLE accounts (name VARCHAR(255), cmnd VARCHAR(255) , account_number VARCHAR(255),balance INT, PRIMARY KEY(account_number));' \
          '' \
          '' \
          ''


    mycursor.execute(sql)
    mydb.commit()

if __name__ == "__main__":
    DataUpdate("aa","bb","cc")
