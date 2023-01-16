import sqlite3
from flask import Flask,redirect, url_for, render_template , request,session

def register_user_to_db(username, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users(username,password) values (?,?)',(username,password))
    con.commit()
    con.close()

def check_user(username,password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT username,password from users where username=? and password=?',(username,password))


    result = cur.fetchone()
    if result:
         return True
    else:
        return False   


app = Flask(__name__)
app.secret_key = "r@nd0msk_1"

@app.route("/")
def index():
    return render_template('login.html')

@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        register_user_to_db(username, password)
        return redirect(url_for('index'))

    else:
        return render_template('register.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_user(username, password):
            session['username'] = username
            return render_template('home.html', username = username)
        else:
            return redirect(url_for('index'))

@app.route('/home', methods=['POST', 'GET'])
def home():
    if 'username' in  session:
        return render_template('home.html', username = session['username'])
    else:
        return "Username or password is incorrect"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug=True) 