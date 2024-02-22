import time
import pandas as pd
import sqlite3

# record start time
start = time.time()

# Connect to the SQLite database
conn = sqlite3.connect('company_xyz.db')

# Load tables into DataFrames
df_customer = pd.read_sql_query("SELECT * FROM Customer", conn)
df_sales = pd.read_sql_query("SELECT * FROM Sales", conn)
df_orders = pd.read_sql_query("SELECT * FROM Orders", conn)
df_items = pd.read_sql_query("SELECT * FROM Items", conn)

# Merge DataFrames to create a single DataFrame with necessary information
df = pd.merge(pd.merge(pd.merge(df_customer, df_sales, on='customer_id'), df_orders, on='sales_id'), df_items, on='item_id')

# Filter by age and non-null, non-zero quantities
df_filtered = df[(df['age'] >= 18) & (df['age'] <= 35) & (df['quantity'] > 0)]

# Group by customer, age, and item to sum the quantities
df_grouped = df_filtered.groupby(['customer_id', 'age', 'item_name']).agg({'quantity': 'sum'}).reset_index()

# Rename columns to match required output
df_grouped.columns = ['Customer', 'Age', 'Item', 'Quantity']

# Save to CSV file with semicolon delimiter
df_grouped.to_csv('output_using_pandas.csv', sep=';', index=False)

print("Data successfully written to output csv file")

# record end time
end = time.time()

# print the difference between start and end time in milli secs
print("The time of execution of above program is :",(end-start) * 10**3, "ms")
