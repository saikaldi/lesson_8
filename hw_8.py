
import sqlite3

def create_connection(db_name):
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(e)

sql_create_countries_table = '''
    CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title VARCHAR(200) NOT NULL
)
'''

def insert_country(conn, country):
    sql = '''INSERT INTO countries(title)
    VALUES(?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, country)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

sql_create_cities_table = '''
    CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    area REAL DEFAULT 0,
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES countries (id)
    )
'''

def insert_cities(conn, city):
    sql = '''INSERT INTO cities(title)
    VALUES(?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, city)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

sql_create_employees_table = '''
    CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(200) NOT NULL,
    last_name VARCHAR(200) NOT NULL,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities (id)
    )
'''

def insert_employee(conn, employee):
    sql = '''INSERT INTO employees(first_name, last_name, city_id)
    VALUES(?,?,?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, employee)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def display_employees_by_city(conn, city_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.first_name, e.last_name, c.title AS city_name, co.title AS country_name, c.area
            FROM employees AS e
            JOIN cities AS c ON e.city_id = c.id
            JOIN countries AS co ON c.country_id = co.id
            WHERE c.id = ?
        """, (city_id,))

        employees = cursor.fetchall()

        if not employees:
            print("No employees found in the selected city.")
        else:
            print("Employees in the selected city:")
            for employee in employees:
                print(
                    f"Name: {employee[0]} {employee[1]}, City: {employee[2]}, Country: {employee[3]}, Area: {employee[4]}")
    except sqlite3.Error as e:
        print(e)

connection = create_connection('hw_8.db')

if connection is not None:
    print('Successfully connected to the database!')


    # create_table(connection, sql_create_countries_table)
    #
    # insert_country(connection, ('Country1',))
    # insert_country(connection, ('Country2',))
    # insert_country(connection, ('Country3',))
    #
    # create_table(connection, sql_create_cities_table)
    # insert_cities(connection, ('Bishkek',))
    # insert_cities(connection, ('Pekin',))
    # insert_cities(connection, ('Rome',))
    # insert_cities(connection, ('Moscow',))
    # insert_cities(connection, ('Berlin',))
    # insert_cities(connection, ('Paris',))
    # insert_cities(connection, ('Vena',))
    #
    # create_table(connection, sql_create_employees_table)
    # insert_employee(connection, ('Sasha','Li',4))
    # employees_data = [
    #     ('John', 'Doe', 3),
    #     ('Alice', 'Smith', 2),
    #     ('Bob', 'Johnson', 5),
    #     ('Emma', 'Brown', 1),
    #     ('Michael', 'Davis', 4),
    #     ('Olivia', 'Wilson', 3),
    #     ('William', 'Lee', 2),
    #     ('Sophia', 'Moore', 5),
    #     ('James', 'Taylor', 1),
    #     ('Mia', 'Anderson', 4),
    #     ('Ethan', 'White', 3),
    #     ('Ava', 'Martin', 2),
    #     ('Noah', 'Harris', 5),
    #     ('Charlotte', 'Clark', 1)
    # ]
    # for i in employees_data:
    #     insert_employee(connection, i)

    while True:
        print("You can display a list of employees by selecting a city ID from the list below. To exit, enter 0:")
        cursor = connection.cursor()
        cursor.execute("SELECT id, title FROM cities")
        cities = cursor.fetchall()
        for city in cities:
            print(f"ID: {city[0]}, City: {city[1]}")

        selected_city_id = int(input("Enter the ID of the city (0 to exit): "))

        if selected_city_id == 0:
            break
        else:
            display_employees_by_city(connection, selected_city_id)
    connection.close()
else:
    print('Connection to the database failed.')
