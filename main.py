from flask import Flask, render_template, redirect, request
import sqlite3
from sqlite3 import Error
from flask_bcrypt import bcrypt
from flask import session

# Create a Flask app
app = Flask(__name__, template_folder='templates')

DATABASE = "zeds_threads.db"

def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

@app.route('/')
def render_homepage():
  return render_template('index.html')
  
@app.route('/shopnow.html')
def render_database():
    con = create_connection(DATABASE)
    if con:
        query = "SELECT name, main_colours, price FROM clothing_data"
        cur = con.cursor()
        cur.execute(query)
        clothing_list = cur.fetchall()
        con.close()
      
        for clothing in clothing_list:
            print(clothing)  
        return render_template('shopnow.html', clothing=clothing_list)
    else:
        return "Error"


@app.route('/login', methods = ['POST', 'GET'])
def render_login_page():
  if is_logged_in():
    return redirect('/products/1')
  print("Logging in")
  if request.method == 'POST':
    print(request.form)
    email = request.form['email'].strip().lower()
    password = request.form['password'].strip()
    print(email)
    query = "SELECT id, fname, password FROM user WHERE email =?"

    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (email,))
    user_data = cur.fetchone() #only one value
    con.close()
    #if the given email is not in the database it will raise an error
    if user_data is None:
      return redirect("/login?error=Email+invalid+or+password+incorrect")
      return render_template("/login?error=Email+invalid+or+password+incorrect")


    try:
      user_id = user_data[0]
      first_name = user_data[1]
      db_password = user_data[2]
    except IndexError:
      return redirect("/login?error=Email+invalid+or+password+incorrect")

    if not bcrypt.check_password_hash(db_password, password):
      return redirect(request.referrer + "?error=Email+invalid+or+password+incorrect")

    session['email'] = email
    session['user_id'] = user_id
    session['firstname'] = first_name

    print(session)
    return redirect('/')

  return render_template('login.html',logged_in = is_logged_in())

@app.route('/logout') #logout function
def logout():
  print(list(session.keys()))
  [session.pop(key) for key in list(session.keys())]
  print(list(session.keys()))
  return redirect('/message=See+you+next+time!')
  return render_template('login.html')


@app.route('/signup', methods = ['POST', 'GET'])
def render_signup_page():
  if request.method == 'POST':
    print(request.form)
    fname = request.form.get('fname').title().strip()
    lname = request.form.get('lname').title().strip()
    email = request.form.get('email').lower().strip()
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if password != password2:
      return redirect("/signup?error=Passwords+do+not+match")

    if len(password) < 8:
      return redirect("/signup?error=Password+must+be+at+least+8+characters")
    hashed_password = bcrypt.generate_password_hash(password)  #creating a hash password
    print(hashed_password)  
    con = create_connection(DATABASE)
    query = "INSERT INTO user(fname, lname, email, password) VALUES(?, ?, ?, ?)"
    cur = con.cursor()

    try:
      cur.execute(query, (fname, lname, email, hashed_password)) #this line actually executes the query
    except sqlite3.IntegrityError:
      con.close()
      return redirect('/signup?error=Email+is+already+used')

    con.commit()  
    con.close()

    return redirect("/login")
  return render_template('signup.html')

def is_logged_in():
  if session.get("email") is None:
    print("not logged in")
    return False
  else:
    print("logged in")
    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
