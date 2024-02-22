import sqlite3

# Connect to SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect('company_xyz.db')
cursor = conn.cursor()

# Create tables
cursor.execute("CREATE TABLE IF NOT EXISTS Customer (customer_id INT PRIMARY KEY, age INT);")
cursor.execute("CREATE TABLE IF NOT EXISTS Sales (sales_id INT PRIMARY KEY, customer_id INT, FOREIGN KEY (customer_id) REFERENCES Customer(customer_id));")
cursor.execute("CREATE TABLE IF NOT EXISTS Items (item_id INT PRIMARY KEY, item_name VARCHAR(255));")
cursor.execute("""CREATE TABLE IF NOT EXISTS Orders (
                    order_id INT PRIMARY KEY, 
                    sales_id INT, 
                    item_id INT, 
                    quantity INT, 
                    FOREIGN KEY (sales_id) REFERENCES Sales(sales_id), 
                    FOREIGN KEY (item_id) REFERENCES Items(item_id)
                  );""")

# Inserting dummy data
# Customers
customers = [(1, 21), (2, 23), (3, 35)]
cursor.executemany("INSERT INTO Customer (customer_id, age) VALUES (?, ?);", customers)

# Sales
sales = [(1, 1), (2, 2), (3, 3)]
cursor.executemany("INSERT INTO Sales (sales_id, customer_id) VALUES (?, ?);", sales)

# Items
items = [(1, 'x'), (2, 'y'), (3, 'z')]
cursor.executemany("INSERT INTO Items (item_id, item_name) VALUES (?, ?);", items)

# Orders
# Note: Using NULL for quantity as per the given rule, but in practice, you might skip these entries or use 0.
orders = [
    (1, 1, 1, 10),  # Customer 1, Item X, Quantity 10
    (2, 1, 2, 0),   # Customer 1, Item Y, Quantity 0
    (3, 1, 3, 0),   # Customer 1, Item Z, Quantity 0
    (4, 2, 1, 1),   # Customer 2, Item X, Quantity 1
    (5, 2, 2, 1),   # Customer 2, Item Y, Quantity 1
    (6, 2, 3, 0),   # Customer 2, Item Z, Quantity 0
    (7, 3, 1, 0),   # Customer 3, Item X, Quantity 0
    (8, 3, 2, 0),   # Customer 3, Item Y, Quantity 0
    (9, 3, 3, 2)    # Customer 3, Item Z, Quantity 2
]
cursor.executemany("INSERT INTO Orders (order_id, sales_id, item_id, quantity) VALUES (?, ?, ?, ?);", orders)

# Commit changes and close connection
conn.commit()
conn.close()

print("Dummy data inserted successfully.")