-- examples/schema.sql
-- Production Database Schema for Retail Analytics
CREATE TABLE
    customers (
        customer_id INT PRIMARY KEY,
        customer_name VARCHAR(100),
        region VARCHAR(50),
        loyalty_status VARCHAR(20)
    );

CREATE TABLE
    raw_sales_data (
        sale_id INT PRIMARY KEY,
        customer_id INT,
        product_id INT,
        date DATE,
        amount DECIMAL(10, 2),
        status VARCHAR(20),
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );