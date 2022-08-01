import sqlite3

conn = sqlite3.connect('/Users/rajithak/PycharmProjects/flashWaterBottleProj/database/waterbottleproj.db')
print ("Opened database successfully");


conn.execute('CREATE TABLE USERS (userid integer, username TEXT, password TEXT, state TEXT)')
print("USERS Table created successfully");
conn.execute('CREATE TABLE WATER_PACKAGES (packageid integer, desc TEXT, bottles_count integer)')
print("WATER_PACKAGES Table created successfully");
conn.execute('CREATE TABLE WATER_STORAGE (storageid integer, userid integer, packageid integer, purchase_date TEXT, consumed_date TEXT, is_empty boolean)')
print("WATER_STORAGE Table created successfully");
conn.execute('CREATE TABLE WATER_CONSUMPTION (storageid integer,  recycled_date TEXT, bottles_recycled integer)')
print ("Users WATER_CONSUMPTION created successfully");

cur = conn.cursor()
cur.execute("INSERT INTO WATER_PACKAGES (packageid,desc, bottles_count) VALUES (?,?,?)",(1,"poland spring 24 pack",24) )
cur.execute("INSERT INTO WATER_PACKAGES (packageid,desc, bottles_count) VALUES (?,?,?)",(2,"poland spring 30 pack",30) )
cur.execute("INSERT INTO WATER_PACKAGES (packageid,desc, bottles_count) VALUES (?,?,?)",(3,"poland spring 12 pack",12) )
conn.commit()
conn.close()
