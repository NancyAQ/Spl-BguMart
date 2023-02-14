import sqlite3
import atexit
from dbtools import Dao
 
# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name,salary,branche):
        self.id=id
        self.name=name
        self.salary=salary
        self.branche=branche
    def __str__(self):
        return '(' + str(self.id) + ', \'' + self.name.decode() + '\', ' + str(self.salary) + ', ' + str(self.branche) + ')'

 
class Supplier(object):
    def __init__(self, id, name,contact_information):
        self.id=id
        self.name=name
        self.contact_information=contact_information
    def __str__(self):
        return '(' + str(self.id) + ', \'' + self.name.decode() + '\', \'' + self.contact_information.decode() + '\')'



class Product(object):
    def __init__(self, id, description,price,quantity):
        self.id=id
        self.description=description
        self.price=price
        self.quantity=quantity
    def __str__(self):
        return '(' + str(self.id) + ', \'' + self.description.decode() + '\', ' + str(self.price) + ', ' + str(self.quantity) + ')'

    def return_quantity(self):
        return self.quantity
    

class Branche(object):
    def __init__(self, id, location,number_of_employees):
        self.id=id
        self.location=location
        self.number_of_employees=number_of_employees
    def __str__(self):
        return '(' + str(self.id) + ', \'' + self.location.decode() + '\', ' + str(self.number_of_employees) + ')'


class Activitie(object):
    def __init__(self, product_id, quantity,activator_id,date):
        self.product_id=product_id
        self.quantity=quantity
        self.activator_id=activator_id
        self.date=date
    def __str__(self):
        return '(' + str(self.product_id) + ', ' + str(self.quantity) + ', ' + str(self.activator_id) + ', \'' + self.date.decode() + '\')'
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self._conn.text_factory = bytes
        #Added
        self.employees=Dao(Employee,self._conn)
        self.suppliers=Dao(Supplier,self._conn)
        self.products=Dao(Product,self._conn)
        self.branches=Dao(Branche,self._conn)
        self.activities=Dao(Activitie,self._conn)
        
 
    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
            
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
    def find_employees_report(self):
        c = self._conn.cursor()
        c.execute('''WITH 
        sales AS (
            SELECT activator_id, SUM(CASE WHEN a.quantity < 0 THEN a.quantity*(-1)*p.price ELSE 0 END) as sales_income
            FROM activities a
            JOIN products p ON a.product_id = p.id
            GROUP BY activator_id
        ),
        employees_sales AS (
            SELECT e.id, e.name, e.salary, b.location as working_location, COALESCE(s.sales_income, 0) as sales_income
            FROM employees e
            JOIN branches b ON e.branche = b.id
            LEFT JOIN sales s ON e.id = s.activator_id
        )
        SELECT name, salary, working_location, sales_income FROM employees_sales 
        ORDER BY name ASC;''')
        print("Employees report")
        for row in c.fetchall():
            print(row[0].decode(),row[1],row[2].decode(),row[3])
    def find_activity_report(self):
        c = self._conn.cursor()
        c.execute('''
            SELECT activities.date, products.description, activities.quantity, 
            CASE WHEN activities.quantity < 0 THEN employees.name ELSE NULL END as seller,
            CASE WHEN activities.quantity >0 THEN suppliers.name ELSE NULL END as supplier
            FROM activities
            LEFT JOIN products ON activities.product_id = products.id
            LEFT JOIN employees ON activities.activator_id = employees.id
            LEFT JOIN suppliers ON activities.activator_id = suppliers.id
            ORDER BY activities.date ASC;
        ''')
        print("Activities report")
        for row in c.fetchall():
            if(row[0]):
                date = '\'' + row[0].decode() +'\''+ ','
            else:date='None'
            if(row[1]):
                fruit = '\'' + row[1].decode()+ '\'' +','
            else:fruit='None'
            if(row[2]):
                quantity = str(row[2])+','
            else:quantity='None'
            if(row[3]):
                seller = '\'' + row[3].decode()+ '\'' +','
            else:seller='None'+','
            if(row[4]):
                supplier = '\'' + row[4].decode() + '\''
            else:supplier='None'
             
            print('('+date,fruit,quantity,seller,supplier+ ')')

 
# singleton
repo = Repository()
atexit.register(repo._close)