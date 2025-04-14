from mysql.connector import Error
from database import openConnection
from faker import Faker
import random

def importTestStaff(times):
    for t in range(1, times+1):
        name = Faker().name()
        sex = 'M' if random.randrange(0,2) == 1 else 'F'
        role = random.randrange(1, 8)
        hours = random.randrange(1, 5)*8
        
        args = [name, sex, role, hours]
        try:
            connection = openConnection()
            cursor = connection.cursor()

            print(f'{t} {args}')
            cursor.execute('call AddStaff(%s, %s, %s, %s)', args)
            cursor.fetchall()

            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error at count {t}: {e}")
            return
    
    cursor.close()
    connection.close()

def importTestOrders(times):
    for t in range(1, times+1):
        order = 1
        staff = 1
        item = random.randrange(1, 12)
        colour = random.randrange(1, 5)
        size = 1
        quantity = random.randrange(1, 30)
        bought = random.randrange(0,2)
        date = '2020-02-02'
        reissue = None if bought == 1 else '2022-02-02' if random.randrange(0,2) == 1 else '2220-02-02'

        
        args = [order, staff, item, colour, size, quantity, bought, date, reissue]
        try:
            connection = openConnection()
            cursor = connection.cursor()

            print(f'{t} {args}')
            cursor.execute("insert into tbl_orders(order_number, staff_id, item_id, colour_id, size, quantity, bought, order_date, reissue_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", args)
            cursor.fetchall()

            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error at count {t}: {e}")
            return
    
    cursor.close()
    connection.close()