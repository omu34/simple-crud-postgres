from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2.extras
import psycopg2
import re

conn = psycopg2.connect(dbname="items", 
                        user="postgres", 
                        password="5599emoyo", 
                        host="localhost"
                        )
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

conn.autocommit = True

app = Flask(__name__)

app.secret_key = "bernardomuse"

@app.route('/')
def index():
    if 'loggedin' in session:    
        cur.execute('SELECT * FROM item2')
        items = cur.fetchall()    
        return render_template('index.html', items=items)
    return redirect(url_for('login'))


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method != "POST":
        return    
    name = request.form["name"]
    bacodes = request.form["bacodes"]
    price = request.form["price"]
    description = request.form["description"]

    cur.execute('''INSERT INTO item2(name, bacodes, price, description) VALUES(%s,%s,%s,%s)''', 
        (name, bacodes, price, description))
    conn.commit()
    flash('Item added successful')
    return redirect(url_for('index'))


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):   
    cur.execute('SELECT * FROM item2 WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', item2=data[0])


@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    cur.execute('SELECT * FROM item2')
    if request.method != "POST":
        return     
    name = request.form["name"]
    bacodes = request.form["bacodes"]
    price = request.form["price"]
    description = request.form["description"]

    cur.execute("""
                    UPDATE item2
                    SET     name=%s, 
                            bacodes=%s, 
                            price=%s,
                            description=%s                         
                    WHERE   id= %s""",
                    (name, bacodes, price, description, id))
    flash("update was successful")
    conn.commit()
    return redirect(url_for('index'))


@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete(id):
    cur.execute('DELETE FROM item2 WHERE id={0}'.format(id))
    conn.commit()
    flash('Successfully deleted')
    return redirect(url_for("index"))


@app.route('/login', methods=['GET', 'POST'])
def login():       
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur.execute('SELECT * FROM signup WHERE username = %s', (username,))
        if account := cur.fetchone():
            password2 = account['password']
            if check_password_hash(password2, password):                
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']                
                return redirect(url_for('index'))
            else:                
                flash('Incorrect username/password')
    elif request.method != 'POST':
        flash('Please sign in the form!')
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])
def register():     
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password)
        cur.execute('SELECT * FROM signup WHERE username = %s', (username,))
        if account := cur.fetchone():
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
                flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
                flash('Please fill out the form!')

        else:
            cur.execute('INSERT INTO signup (fullname,username, password, email) VALUES (%s,%s,%s,%s)',
            (fullname, username, hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
            return redirect(url_for('index'))
    elif request.method != 'POST':
        flash('Please fill out the form!')       

    return render_template('register.html')   
   
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))
  




if __name__ == '__main__':
    app.run(debug=True)
