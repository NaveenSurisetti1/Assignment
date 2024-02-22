import time
import sqlite3
import csv

# record start time
start = time.time()

# Path to your SQLite database
db_path = 'company_xyz.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL query to extract total quantities of each item bought per customer aged 18-35
query = """
SELECT 
    c.customer_id AS Customer,
    c.age AS Age,
    i.item_name AS Item,
    SUM(o.quantity) AS Quantity
FROM 
    Customer c
JOIN 
    Sales s ON c.customer_id = s.customer_id
JOIN 
    Orders o ON s.sales_id = o.sales_id
JOIN 
    Items i ON o.item_id = i.item_id
WHERE 
    c.age BETWEEN 18 AND 35 AND o.quantity > 0
GROUP BY 
    c.customer_id, c.age, i.item_name
HAVING 
    SUM(o.quantity) > 0
ORDER BY 
    c.customer_id, i.item_name;
"""

# Execute the query
cursor.execute(query)

# Fetch all rows of the query result
rows = cursor.fetchall()

# Define CSV file path (update 'output.csv' to your desired path)
output_csv_path = 'output_using_sql_without_pandas.csv'

# Write to CSV file with semicolon delimiter
with open(output_csv_path, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    # Write the header
    writer.writerow(['Customer', 'Age', 'Item', 'Quantity'])
    # Write the data
    writer.writerows(rows)

# Close the connection to the database
conn.close()

print(f"Data successfully written to {output_csv_path}")

# record end time
end = time.time()

# print the difference between start and end time in milli secs
print("The time of execution of above program is :",(end-start) * 10**3, "ms")