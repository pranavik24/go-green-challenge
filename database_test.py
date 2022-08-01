import sqlite3

con = sqlite3.connect('/Users/rajithak/PycharmProjects/flashWaterBottleProj/database/waterbottleproj.db')
print ("Opened database successfully");

con.row_factory = sqlite3.Row

cur = con.cursor()
# cur.execute( "select u.username, u.state, wc.storageid, SUM(wc.bottles_recycled) as bottles_recycled,  "
#              "wp.bottles_count, wp.desc from WATER_CONSUMPTION wc, USERS u, WATER_PACKAGES wp, WATER_STORAGE ws "
#              "where wc.storageid = ws.storageid and ws.is_empty = 1 and ws.userid = u.userid and "
#              "ws.packageid = wp.packageid group by u.username, u.state, wc.storageid, wp.bottles_count, wp.desc")
cur.execute("select username, state, sum(bottles_recycled) as bottles_recycled, sum(bottles_count) as bottles_count, "
            " (SUM(bottles_recycled)*100)/sum(bottles_count) as score from ("
            " select u.username, u.state, ws.storageid, SUM(wc.bottles_recycled)  as bottles_recycled,  "
                "wp.bottles_count "
                "from WATER_CONSUMPTION wc, USERS u, WATER_PACKAGES wp, WATER_STORAGE ws "
                "where wc.storageid = ws.storageid and ws.is_empty = 1 and ws.userid = u.userid and "
                "ws.packageid = wp.packageid group by u.username, u.state , ws.storageid ) bottles"
            " group by username, state"
            " order by score desc")


# cur.execute( "select  wc.storageid, SUM(wc.bottles_recycled) as bottles_recycled  "
#              " from WATER_CONSUMPTION wc, USERS u, WATER_PACKAGES wp, WATER_STORAGE ws "
#              "where wc.storageid = ws.storageid and ws.is_empty = 1 and ws.userid = u.userid and "
#              "ws.packageid = wp.packageid group by u.username, u.state, wc.storageid, wp.bottles_count, wp.desc")
#cur.execute("select * from  WATER_PACKAGES")
rows = cur.fetchall()
for r in rows:
    for i in r:
        print(i, end=", ")
    print("")
# return render_template("list.html", rows=rows)
