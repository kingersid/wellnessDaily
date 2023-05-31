import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('blog2.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the table to store tags
# Execute the DELETE query to remove all rows from the table
table_name = 'post'
delete_query = f"DELETE FROM {table_name}"
cursor.execute(delete_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

