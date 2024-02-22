import time
import sqlite3
import pandas as pd

# record start time
start = time.time()

# Path to the SQLite database
db_path = 'company_xyz.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

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
    c.age BETWEEN 18 AND 35 AND o.quantity IS NOT NULL
GROUP BY 
    c.customer_id, c.age, i.item_id
HAVING 
    SUM(o.quantity) > 0
ORDER BY 
    c.customer_id, i.item_id;
"""

# Execute the SQL query and load the results into a Pandas DataFrame
df = pd.read_sql_query(query, conn)

# Close the connection to the database
conn.close()

# Save the DataFrame to a CSV file with semicolon delimiter
output_csv_path = 'output_using_sql_with_pandas.csv'
df.to_csv(output_csv_path, sep=';', index=False)

print(f"Data successfully written to {output_csv_path}")

# record end time
end = time.time()

# print the difference between start and end time in milli secs
print("The time of execution of above program is :",(end-start) * 10**3, "ms")