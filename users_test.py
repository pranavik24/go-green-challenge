import sqlite3

con = sqlite3.connect('/Users/rajithak/PycharmProjects/flashWaterBottleProj/database/waterbottleproj.db')
print ("Opened database successfully");

con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute("select * from  USERS")
rows = cur.fetchall()
for r in rows:
    print(r[0],end=', ')
    print(r[1],end=', ')
    print(r[2],end=', ')
    print(r[3])

cur.execute("select * from  WATER_STORAGE")
rows = cur.fetchall()
for r in rows:
    print(r[0], end=', ')
    print(r[1], end=', ')
    print(r[2], end=', ')
    print(r[3], end=', ')
    print(r[4], end=', ')
    print(r[5])

cur.execute("select * from  WATER_CONSUMPTION")
rows = cur.fetchall()
for r in rows:
    print(r[0],end=', ')
    print(r[1],end=', ')
    print(r[2])

print("printed users, water storage, water consump")


