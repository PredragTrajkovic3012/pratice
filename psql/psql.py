import psycopg2

con = psycopg2.connect(
    host='localhost',
    database='projekat',
    user='predrag',
    password='123')

#cursor
cur = con.cursor()

# execute the query
cur.execute('Select * from tbl')

rows = cur.fetchall()

for r in rows:
    print(f"xxx {r[0]} yyy {r[1]}")

# close the cursor
cur.close()

# close the connection
con.close()