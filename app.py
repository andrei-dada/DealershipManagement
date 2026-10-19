import mysql.connector
import os
import time
import subprocess
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()
# -----------------------------#
#            Flask             #
# -----------------------------#
app = Flask(__name__)

print("Starting MySQL server from Docker...") 

#Start docker
subprocess.run(["docker", "compose", "up", "-d"])




# -------------------------------#
#   Loading until MySQL is ready #
# -------------------------------#
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

print("✅ MySQL is ready!")

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
# GET, POST ,PUT, DELETE employees
# -----------------------------
# -----------------------------
# CREATE (POST)
# -----------------------------
@app.route("/employees", methods=["POST"])
def add_employees():
    data = request.get_json()  # ! it's a list of dictionaries
    if isinstance(data, dict): 
        data = [data]
    conn = get_db_connection()
    cursor = conn.cursor()

    for employee in data:
        # * extract the fields for each employee
        last_name = employee["last_name"]  # * read the last name
        first_name = employee["first_name"]  # * read the first name
        hire_date = employee.get("hire_date")  # * if missing, the DEFAULT is used

        # * insert the employee into the table
        cursor.execute(
            "INSERT INTO employees (last_name, first_name, hire_date) VALUES (%s, %s, %s)",
            (last_name, first_name, hire_date)
        )
        conn.commit()  # ! commit for each insert, so we save immediately

    cursor.close()  # ! close the cursor
    conn.close()    # ! close the connection
    return jsonify({"message": f"{len(data)} employees added successfully!"}), 201

# -----------------------------
# READ (GET)
# -----------------------------
@app.route("/employees", methods=["GET"])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)




# -----------------------------
# UPDATE (PUT)
# -----------------------------
@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json()
    last_name = data["last_name"]
    first_name = data["first_name"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employees SET last_name=%s, first_name=%s WHERE employee_id=%s",
        (last_name, first_name, employee_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Employee updated!"}), 200



# -----------------------------
# DELETE (DELETE)
# -----------------------------
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE employee_id=%s", (employee_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Employee deleted!"}), 200




# -----------------------------
# CREATE (POST)
# -----------------------------
@app.route("/clients", methods=["POST"])
def add_clients():
    data = request.get_json()  # ! it's a list of dictionaries
    if isinstance(data, dict): 
        data = [data]
    conn = get_db_connection()
    cursor = conn.cursor()

    for client in data:
        # * extract the fields for each client
        last_name = client["last_name"]  # * read the last name
        first_name = client["first_name"]  # * read the first name
        email = client.get("email")  # * read email, may be missing
        phone = client.get("phone")  # * read phone, may be missing

        # * insert the client into the table
        cursor.execute(
            "INSERT INTO clients (last_name, first_name, email, phone) VALUES (%s, %s, %s, %s)",
            (last_name, first_name, email, phone)
        )
        conn.commit()  # ! commit for each insert

    cursor.close()  # ! close the cursor
    conn.close()    # ! close the connection
    return jsonify({"message": f"{len(data)} clients added successfully!"}), 201



# -----------------------------
# READ (GET)
# -----------------------------
@app.route("/clients", methods=["GET"])
def get_clients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


# -----------------------------
# UPDATE (PUT)
# -----------------------------
@app.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    data = request.get_json()
    last_name = data["last_name"]
    first_name = data["first_name"]
    email = data["email"]
    phone = data["phone"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clients SET last_name=%s, first_name=%s, email=%s, phone=%s WHERE client_id=%s",
        (last_name, first_name, email, phone, client_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Client updated!"}), 200


# -----------------------------
# DELETE (DELETE)
# -----------------------------
@app.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE client_id=%s", (client_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Client deleted!"}), 200





@app.route("/cars", methods=["POST"])
def add_cars():
    data = request.get_json()  # ! it's a list of dictionaries
    if isinstance(data, dict): 
        data = [data]
    conn = get_db_connection()
    cursor = conn.cursor()

    for car in data:
        # * extract the fields for each car
        vin = car["vin"]  # * read the VIN
        make = car["make"]  # * read the make
        model = car["model"]  # * read the model
        manufacture_year = car["manufacture_year"]  # * read the manufacturing year
        price = car["price"]  # * read the price
        available = car.get("available", True)  # * default TRUE if not specified

        # * insert the car into the table
        cursor.execute(
            "INSERT INTO cars (vin, make, model, manufacture_year, price, available) VALUES (%s, %s, %s, %s, %s, %s)",
            (vin, make, model, manufacture_year, price, available)
        )
        conn.commit()  # ! commit for each insert

    cursor.close()  # ! close the cursor
    conn.close()    # ! close the connection
    return jsonify({"message": f"{len(data)} cars added successfully!"}), 201

# READ
@app.route("/cars", methods=["GET"])
def get_cars():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cars")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


@app.route("/sales", methods=["POST"])
def add_sale():
    data = request.get_json()  # can be a dictionary or a list
    if isinstance(data, dict):
        data = [data]

    conn = get_db_connection()
    cursor = conn.cursor()

    for sale in data:
        car_id = sale["car_id"]
        employee_id = sale["employee_id"]
        client_id = sale["client_id"]
        sale_date = sale.get("sale_date")
        sale_price = sale["sale_price"]

        # Check whether the car is available
        cursor.execute("SELECT available FROM cars WHERE car_id = %s", (car_id,))
        car = cursor.fetchone()

        if not car:
            cursor.close()
            conn.close()
            return jsonify({"error": f"Car with id {car_id} does not exist!"}), 400

        if not car[0]:
            cursor.close()
            conn.close()
            return jsonify({"error": f"Car with id {car_id} is not available!"}), 400

        # Insert the sale
        cursor.execute(
            "INSERT INTO sales (car_id, employee_id, client_id, sale_date, sale_price) VALUES (%s, %s, %s, %s, %s)",
            (car_id, employee_id, client_id, sale_date, sale_price)
        )
        conn.commit()

        # Mark the car as unavailable
        cursor.execute(
            "UPDATE cars SET available = FALSE WHERE car_id = %s",
            (car_id,)
        )
        conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": f"{len(data)} sales added successfully!"}), 201





@app.route("/sales", methods=["GET"])
def get_sales():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route("/sales/<int:sale_id>", methods = ["DELETE"])
def delete_sale(sale_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sales WHERE sale_id=%s", (sale_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Sale deleted!"}), 200


# -----------------------------
# Start flask
# -----------------------------
if __name__ == "__main__":
    print("🔌 Connecting to MySQL...")
    try:
        conn = get_db_connection()
        if conn.is_connected():
            print("Successfully connected to the database!")
        conn.close()
    except Exception as e:
        print("Connection error:", e)

    print("Starting Flask at http://127.0.0.1:5001")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False) # ! use_reloader=False to avoid duplicating Docker processes!
                                            # ! otherwise we'd have 2 Docker containers and it would error that one already exists
                                            # ! with the same name.