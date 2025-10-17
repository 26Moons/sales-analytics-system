--DataBase Initialization Script ( Day 1 )

CREATE SCHEMA IF NOT EXISTS sales_data;
CREATE TABLE IF NOT EXISTS sales_data.transactions (
    transaction_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_date DATE,
    region VARCHAR(25),
    product VARCHAR(50),
    quantity INT,
    unit_price NUMERIC(10,2),
    total_sales NUMERIC(12,2)
);

INSERT INTO sales_data.transactions (order_date,region,product,quantity,unit_price,total_sales)
VALUES
('2024-01-05', 'North', 'Laptop', 5, 55000, 275000),
('2024-01-07', 'South', 'Mobile', 10, 15000, 150000),
('2024-01-10', 'West', 'Tablet', 3, 30000, 90000)
