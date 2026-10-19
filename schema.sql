CREATE DATABASE IF NOT EXISTS dealership;
USE dealership;

CREATE TABLE IF NOT EXISTS employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    last_name   VARCHAR(100) NOT NULL,
    first_name  VARCHAR(100) NOT NULL,
    hire_date   DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS clients (
    client_id  INT AUTO_INCREMENT PRIMARY KEY,
    last_name  VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    email      VARCHAR(150),
    phone      VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS cars (
    car_id           INT AUTO_INCREMENT PRIMARY KEY,
    vin              VARCHAR(17) NOT NULL UNIQUE,
    make             VARCHAR(50) NOT NULL,
    model            VARCHAR(50) NOT NULL,
    manufacture_year INT,
    price            DECIMAL(10,2),
    available        BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id     INT AUTO_INCREMENT PRIMARY KEY,
    car_id      INT NOT NULL,
    employee_id INT NOT NULL,
    client_id   INT NOT NULL,
    sale_date   DATE,
    sale_price  DECIMAL(10,2),
    FOREIGN KEY (car_id)        REFERENCES cars(car_id),
    FOREIGN KEY (employee_id)   REFERENCES employees(employee_id),
    FOREIGN KEY (client_id)     REFERENCES clients(client_id)
);