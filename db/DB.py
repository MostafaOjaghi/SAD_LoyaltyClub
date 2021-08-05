# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IwTb3XkL8ynyrWiTw3hN5xadi0xq7F1A

[source](https://www.w3schools.com/python/python_mysql_getstarted.asp)
"""

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'SADProject'

TABLES = {}
TABLES['customerT'] = (
    "CREATE TABLE `customerT` ("
    "  `customerID` VARCHAR(30) PRIMARY KEY,"
    "  `email` VARCHAR(255) NOT NULL,"
    "  `score` INTEGER NOT NULL"
    ") ")
TABLES['orderT'] = (
    "CREATE TABLE `orderT` ("
    "  `orderID` VARCHAR(100) PRIMARY KEY,"
    "  `customerID` VARCHAR(30) NOT NULL,"
    "  `date` DATE NOT NULL,"
    "  `total_price` INTEGER NOT NULL,"
    " FOREIGN KEY (customerID) REFERENCES customerT (customerID)"
    ") ")

class DBClass:
    def __init__(self):
        cnx = mysql.connector.connect(
            host="localhost",
            user="sad",
            password="sad_pass",
            database="SADProject"
            )

        cursor = cnx.cursor()
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
    
        cursor.close()
        self.cnx = cnx

    def insert_customer(self, params):
        id = params['customerID']
        email = params['email']
        score = 0;

        sql = "INSERT INTO customerT (customerID, email, score) VALUES (%s, %s, %s)"
        val = (id, email, score)
        cursor = self.cnx.cursor()
        cursor.execute(sql, val)
        self.cnx.commit()
        cursor.close()

    def insert_order(self, params):
        order_id = params['orderID']
        customer_id = params['customerID']
        date = params['date']
        total_price = params['total_price']

        sql = "INSERT INTO orderT (orderID, customerID, date, total_price) VALUES (%s, %s, %s, %s)"
        val = (order_id, customer_id, date, total_price)
        cursor = self.cnx.cursor()
        cursor.execute(sql, val)
        self.cnx.commit()
        cursor.close()

    def get_orders(self, user_id):
        sql = "SELECT date, total_price FROM orderT WHERE customerID = %s"
        val = (user_id,)
        cursor = self.cnx.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        result = [dict([('date', date.strftime('%Y/%m/%d')), ('total_price', total_price)])
                for (date, total_price) in result]
        return result
    
    def get_recent_purchases(self, user_id, months):
        sql = "SELECT total_price FROM orderT WHERE customerID = %s \
                AND date >= DATE_SUB( CURDATE(), INTERVAL %s MONTH )"
        val = (user_id, months)
        cursor = self.cnx.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        result = [x[0] for x in result]
        return result

    def get_sum_of_purchases(self, user_id, months):
        sql = "SELECT sum(total_price) FROM orderT \
                WHERE customerID = %s AND date >= DATE_SUB( CURDATE(), INTERVAL %s MONTH )"
        val = (user_id, months)
        cursor = self.cnx.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        sum = result[0][0]
        if not sum:
            sum = 0
        return sum
    
    def get_a_months_sales(self, month):
        sql = "SELECT sum(total_price) FROM orderT \
                WHERE date >= DATE_FORMAT(CURRENT_DATE - INTERVAL %s MONTH, '%Y/%m/01')\
                AND date < DATE_FORMAT(CURRENT_DATE - INTERVAL %s MONTH, '%Y/%m/01')"
        val = (month + 1, month)
        cursor = self.cnx.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        sum = result[0][0]
        if not sum:
            sum = 0
        return int(sum)

    def get_userIDs(self):
        sql = 'SELECT customerID FROM customerT'
        cursor = self.cnx.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        result = [user_id for (user_id,) in result]
        cursor.close()
        return result

    def get_customer_score(self, user_id):
        sql = "SELECT score FROM customerT WHERE customerID = %s"
        val = (user_id,)
        cursor = self.cnx.cursor()
        cursor.execute(sql, val)
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_all_scores(self):
        sql = 'SELECT customerID, score FROM customerT'
        cursor = self.cnx.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        result = dict([(customerID, score) for (customerID, score) in result])
        return result

    def update_customer_score(self, user_id, score):
        sql = "UPDATE customerT SET score = %s WHERE customerID = %s"
        val = (score, user_id)
        cursor = self.cnx.cursor()
        cursor.execute(sql, val)
        self.cnx.commit()
        cursor.close()


if __name__ == "__main__":
    db = DBClass()

    # customer = {
    #     'customerID' : '1233',
    #     'email' : 'a@b.c',
    #     'score' : '0',
    # }
    # db.insert_customer(customer)

    # order = {
    #     'orderID': '001',
    #     'customerID': '1233',
    #     'date': '2021-6-11',
    #     'total_price': '12',
    # }
    # db.insert_order(order)

    orders = db.get_orders('1233')
    print('get_orders:', orders)

    users = db.get_userIDs()
    print('get_userIDs:', users)

    price = db.get_sum_of_purchases('1233', 1)
    print('sum of purchases: ', price)

    purchases = db.get_recent_purchases('1233', 10)
    print('purchases: ', purchases)

    db.update_customer_score('1233', 5)

    scores = db.get_all_scores()
    print('scores:', scores)
