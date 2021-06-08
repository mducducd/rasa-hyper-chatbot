import mysql.connector
from mysql.connector import connection

# cnx = connection.MySQLConnection(user='root', password='root',
#                                  host='localhost',
#                                  database='rasa_hyper')

mydb = mysql.connector.connect(host="localhost", user="root", database="rasa_hyper")
mycursor = mydb.cursor()

def DataUpdate(cust_name,cust_cmnd,account_number, balance):
    # sql = 'SELECT COUNT(ProductID) FROM Products;'
    # balance = 10000000;
    sql='INSERT INTO accounts (full_name, id_card, account_number,balance) VALUES ("{0}","{1}", "{2}","{3}");'.format(cust_name,cust_cmnd,account_number,balance)
    mycursor.execute(sql)
    mydb.commit()

def getBalance(account_number):
    mycursor = mydb.cursor()
    sql='select balance from accounts where account_number={}'.format(account_number)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult[0][0]

def numOfAccounts():
    mycursor = mydb.cursor()
    sql='select count(*) from accounts '
    mycursor.execute(sql)
    myresult = mycursor.fetchone()

    return myresult[0]

def transfer(acc1, acc2, credit):
    if(getBalance(acc1)<credit):
        return
    else:
        newBalance1 = getBalance(acc1) - credit
        newBalance2 = getBalance(acc1) + credit
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE accounts SET balance = {} WHERE account_number = '{}';".format(newBalance1, acc1))
        mycursor.execute("UPDATE accounts SET balance = {} WHERE account_number = '{}';".format(newBalance2, acc2))

        mydb.commit()

def getServiceName():
    # sql = 'CREATE TABLE accounts (name VARCHAR(255), cmnd VARCHAR(255) , account_number VARCHAR(255),balance INT)'
    sql='select service from services'
    mycursor.execute(sql)
    result = mycursor.fetchall();
    mydb.commit()
    return result

# print(getServiceName())

