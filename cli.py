import mysql.connector
import subprocess
import time
import os
from datetime import datetime
from datetime import date
from dotenv import load_dotenv

load_dotenv()
print("Starting MySQL server from Docker...")
subprocess.run(["docker", "compose", "up", "-d"])


while True:
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password=os.getenv("MYSQL_PASSWORD")
        )
        conn.close()
        break
    except:
        print("Loading...", end="\r")  # overwrites the line
        time.sleep(1)
        
print("✔ MySQL is ready!")

# -----------------------------#
#   MySQL connection function  #
# -----------------------------#
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",   # connection to the MySQL container
        port=3306,          # note: your exposed port in Docker
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="dealership"  
    )

# -----------------------------
# CRUD – Employees
# -----------------------------
def add_employee_cli():
    last_name = input("Last name: ")
    first_name = input("First name: ")
    hire_date = input("Hire date (YYYY-MM-DD) or leave empty: ").strip()  # remove spaces
    if hire_date == "":
        hire_date = hire_date = date.today().isoformat()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (last_name, first_name, hire_date) VALUES (%s, %s, %s)",
        (last_name, first_name, hire_date)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Employee added!")


def list_employees_cli():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()


# -----------------------------
# CRUD – Clients
# -----------------------------
def add_client_cli():
    last_name = input("Last name: ")
    first_name = input("First name: ")
    email = input("Email: ")
    phone = input("Phone: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clients (last_name, first_name, email, phone) VALUES (%s, %s, %s, %s)",
        (last_name, first_name, email, phone)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Client added!")


def list_clients_cli():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()


# -----------------------------
# CRUD – Cars
# -----------------------------
def add_car_cli():
    vin = input("VIN: ")
    make = input("Make: ")
    model = input("Model: ")
    year = input("Manufacturing year: ")
    price = input("Price: ")
    available = input("Available (1/0): ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cars (vin, make, model, manufacture_year, price, available) VALUES (%s, %s, %s, %s, %s, %s)",
        (vin, make, model, year, price, available)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Car added!")


def list_cars_cli():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()


# -----------------------------
# CRUD – Sales
# -----------------------------
def add_sale_cli():
    car_id = input("Car ID: ")
    employee_id = input("Employee ID: ")
    client_id = input("Client ID: ")
    sale_date = input("Sale date (YYYY-MM-DD): ")
    sale_price = input("Sale price: ")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sales (car_id, employee_id, client_id, sale_date, sale_price) VALUES (%s, %s, %s, %s, %s)",
        (car_id, employee_id, client_id, sale_date, sale_price)
    )
    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Sale added!")


def list_sales_cli():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sales")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()


# -----------------------------
# Reports
# -----------------------------
def report_sales_period_cli():
    start = input("Start (YYYY-MM-DD): ")
    end = input("End (YYYY-MM-DD): ")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, e.last_name AS emp_last_name, e.first_name AS emp_first_name,
               c.last_name AS client_last_name, car.make, car.model
        FROM sales s
        JOIN employees e ON s.employee_id = e.employee_id
        JOIN clients c ON s.client_id = c.client_id
        JOIN cars car ON s.car_id = car.car_id
        WHERE s.sale_date BETWEEN %s AND %s
    """, (start, end))

    for row in cursor.fetchall():
        print(row)

    cursor.close()
    conn.close()


def report_best_salesperson_cli():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.last_name, e.first_name, COUNT(*) AS total
        FROM sales s
        JOIN employees e ON s.employee_id = e.employee_id
        GROUP BY s.employee_id
        ORDER BY total DESC
        LIMIT 1
    """)

    print(cursor.fetchone())
    cursor.close()
    conn.close()


def report_best_selling_car_cli():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT car.make, car.model, COUNT(*) AS total
        FROM sales s
        JOIN cars car ON s.car_id = car.car_id
        GROUP BY s.car_id
        ORDER BY total DESC
        LIMIT 1
    """)
    print(cursor.fetchone())
    cursor.close()
    conn.close()


def report_total_profit_cli():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(sale_price) FROM sales")
    total = cursor.fetchone()[0]
    print("Total profit:", total if total else 0)
    cursor.close()
    conn.close()


def delete_mysql_container():
    print("\n Stopping the MySQL database...")
    subprocess.run(["docker", "compose", "down"]) # !!! stops and removes the container on exit (keeps the data volume)

# -----------------------------
# Main menu
# -----------------------------
def main_menu():
    while True:
        print("\n====== MAIN MENU ======")
        print("1. Employees")
        print("2. Clients")
        print("3. Cars")
        print("4. Sales")
        print("5. Reports")
        print("0. Exit")
        opt = input("Select: ")

        if opt == "1": menu_employees()
        elif opt == "2": menu_clients()
        elif opt == "3": menu_cars()
        elif opt == "4": menu_sales()
        elif opt == "5": menu_reports()
        elif opt == "0": 
            print("Closing application...")
            delete_mysql_container()
            return
        else: print("Invalid option!")


# -----------------------------
# Sub-menus
# -----------------------------
def menu_employees():
    print("\n--- Employees ---")
    print("1. Add")
    print("2. Show")
    opt = input("Select: ")
    if opt == "1": add_employee_cli()
    elif opt == "2": list_employees_cli()


def menu_clients():
    print("\n--- Clients ---")
    print("1. Add")
    print("2. Show")
    opt = input("Select: ")
    if opt == "1": add_client_cli()
    elif opt == "2": list_clients_cli()


def menu_cars():
    print("\n--- Cars ---")
    print("1. Add")
    print("2. Show")
    opt = input("Select: ")
    if opt == "1": add_car_cli()
    elif opt == "2": list_cars_cli()


def menu_sales():
    print("\n--- Sales ---")
    print("1. Add")
    print("2. Show")
    opt = input("Select: ")
    if opt == "1": add_sale_cli()
    elif opt == "2": list_sales_cli()


def menu_reports():
    print("\n--- Reports ---")
    print("1. Sales in a period")
    print("2. Best salesperson")
    print("3. Best-selling car")
    print("4. Total profit")
    opt = input("Select: ")

    if opt == "1": report_sales_period_cli()
    elif opt == "2": report_best_salesperson_cli()
    elif opt == "3": report_best_selling_car_cli()
    elif opt == "4": report_total_profit_cli()


# -----------------------------
# Main program
# -----------------------------
main_menu()




# tick character copy paste: ✔