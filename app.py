from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "any random string"


def getconn():
    con = sqlite3.connect('/Users/rajithak/PycharmProjects/flashWaterBottleProj/database/waterbottleproj.db')
    con.row_factory = sqlite3.Row
    return con


@app.route('/')
def index_page():  # put application's code here
    return render_template('index.html')


@app.route('/mybottles')
def my_bottles():  # put application's code here
    username = session['uname']
    cur = getconn().cursor()
    print(username)
    cur.execute("select u.username, u.userid, u.state, wc.storageid, SUM(wc.bottles_recycled)  as bottles_recycled,  "
                "wp.bottles_count, (SUM(wc.bottles_recycled)*100)/SUM(wp.bottles_count) as score, wp.desc, ws.purchase_date from "
                "WATER_CONSUMPTION wc, USERS u, WATER_PACKAGES wp, WATER_STORAGE ws "
                "where ws.is_empty = 0 and ws.userid = u.userid and wc.storageid = ws.storageid  and "
                "ws.packageid = wp.packageid and u.username = '" + username + "'" +
                " group by u.username, u.state, wc.storageid, wp.bottles_count, wp.desc")

    rows = cur.fetchall()
    for r in rows:
        for i in r:
            print(i, end=", ")
        print("")
    return render_template('mybottles.html', data=rows)


@app.route('/login', methods=['POST'])
def login():  # put application's code here
    username = request.form['uname']
    password = request.form['psw']
    cur = getconn().cursor()
    cur.execute("select u.password , u.userid from USERS u where u.username = '" + username + "'")
    row = cur.fetchone()
    error = None
    if row is not None:
        # compare db password with user password
        if password == row[0]:
            flash('You were successfully logged in')
            session['uname'] = username
            session['uid'] = row[1]
            return redirect(url_for('my_bottles'))
        else:
            error = "Invalid credentials"
    else:
        error = "Invalid credentials"

    # if success case , redirect to mybottles
    # if fail case, redirect to login fail page
    # flash('Invalid credentials. Please Login again')
    return render_template('index.html', error=error)


def get_storage_id():
    cur = getconn().cursor()
    cur.execute("select ws.storageid from WATER_STORAGE  ws")
    rows = cur.fetchall();
    max = 0;
    for row in rows:
        for r in row:
            if r > max:
                max = r

    return max + 1;

def get_user_id():
    cur = getconn().cursor()
    cur.execute("select u.userid from USERS u")
    rows = cur.fetchall();
    max = 0;
    for row in rows:
        for r in row:
            if r > max:
                max = r

    return max + 1;


@app.route('/addpackage', methods=['POST'])
def add_package():
    print("got add  package ")
    pkid = request.form.get("packages")
    print()
    purchaseDate = request.form['purchasedate']
    print(pkid)
    username = session['uname']
    conn = getconn()
    cur = conn.cursor()
    userid = session['uid']
    storageId = get_storage_id();
    cur.execute(
        "INSERT INTO WATER_STORAGE(storageid,userid, packageid, purchase_date, consumed_date,is_empty)" +
        " VALUES (?,?,?,?,?,?)",
        (storageId, userid, pkid, purchaseDate, None, 0))
    cur.execute("INSERT INTO WATER_CONSUMPTION(storageid, recycled_date,bottles_recycled) VALUES (?,?,?)",
                (storageId, purchaseDate, 0))
    conn.commit()
    conn.close()
    return redirect(url_for('my_bottles'))


@app.route('/addpackagepage')
def add_packages_page():
    cur = getconn().cursor()
    cur.execute("select wp.packageid, wp.bottles_count,  wp.desc from WATER_PACKAGES wp")
    rows = cur.fetchall()
    return render_template('addpackage.html', rows=rows)


@app.route('/addrecycle', methods=['POST'])
def add_recycles():
    print("got recycle  package ")
    recyclePkID = request.form.get("recyclePacks")
    print(recyclePkID)
    recycleNum = request.form['quantity']
    recycleDate = request.form['currDate']
    conn = getconn()
    cur = conn.cursor()
    cur.execute("INSERT INTO WATER_CONSUMPTION(storageid, recycled_date,bottles_recycled) VALUES (?,?,?)",
                (recyclePkID, recycleDate, recycleNum))
    conn.commit()
    conn.close()
    return redirect(url_for('my_bottles'))


@app.route('/addrecyclepage')
def add_recycles_page():
    username = session['uname']
    cur = getconn().cursor()
    print(username)
    cur.execute("select wc.storageid, wp.desc, ws.purchase_date from "
                "WATER_CONSUMPTION wc, USERS u, WATER_PACKAGES wp, WATER_STORAGE ws "
                "where ws.is_empty = 0 and ws.userid = u.userid and wc.storageid = ws.storageid  and "
                "ws.packageid = wp.packageid and u.username = '" + username + "'" +
                " group by u.username, u.state, wc.storageid, wp.bottles_count, wp.desc")
    rows = cur.fetchall()
    for r in rows:
        for i in r:
            print(i, end=", ")
        print("")
    return render_template('addrecycle.html', rows=rows)


@app.route('/addmarkasfin', methods=['POST'])
def add_markasfin():
    print("got mark as fin package")
    delPackID = request.form.get("deletePacks");
    print(delPackID);
    conn = getconn()
    cur = conn.cursor()
    cur.execute("UPDATE WATER_STORAGE  SET is_empty = 1  " 
                " where storageid = " + delPackID)
    conn.commit()
    conn.close()
    return redirect(url_for('my_bottles'))


@app.route('/addmarkasfinpage')
def add_markasfin_pages():
    username = session['uname']
    cur = getconn().cursor()
    print(username)
    cur.execute("select wc.storageid, wp.desc, ws.purchase_date from " 
                "WATER_CONSUMPTION wc, USERS u, WATER_PACKAGES wp, WATER_STORAGE ws " 
                "where ws.is_empty = 0 and ws.userid = u.userid and wc.storageid = ws.storageid  and " 
                "ws.packageid = wp.packageid and u.username = '" + username + "'" 
                " group by u.username, u.state, wc.storageid, wp.bottles_count, wp.desc")
    rows = cur.fetchall()
    return render_template('markasfin.html', rows=rows)


@app.route('/leaderboard')
def leaderboard():  # put application's code here
    cur = getconn().cursor()
    cur.execute(
        "select username, state, sum(bottles_recycled) as bottles_recycled, sum(bottles_count) as bottles_count, "
        " (SUM(bottles_recycled)*100)/sum(bottles_count) as score from ("
        " select u.username, u.state, ws.storageid, SUM(wc.bottles_recycled)  as bottles_recycled,  "
        "wp.bottles_count "
        "from WATER_CONSUMPTION wc, USERS u, WATER_PACKAGES wp, WATER_STORAGE ws "
        "where wc.storageid = ws.storageid and ws.is_empty = 1 and ws.userid = u.userid and "
        "ws.packageid = wp.packageid group by u.username, u.state , ws.storageid ) bottles"
        " group by username, state"
        " order by score desc")

    rows = cur.fetchall()

    return render_template('leaderboard.html', rows=rows)

@app.route('/addsignup')
def add_signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    print("signing up")
    userName = request.form['uname']
    passWord = request.form['password']
    State = request.form['state']

    userID = get_user_id()
    print(userID);
    conn = getconn()
    cur = conn.cursor()
    cur.execute("INSERT INTO USERS(userid,username, password, state) VALUES (?,?,?,?)",(userID,userName,passWord, State))

    conn.commit()
    conn.close()
    print("finished signing up")
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
