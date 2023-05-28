import sqlite3

conn=sqlite3.connect('blog1.db')

cursor = conn.cursor()


update_query = " UPDATE postF SET image = 'skip.png'  WHERE id = 3"

cursor.execute(update_query)

conn.commit()

cursor.close()
conn.close()

