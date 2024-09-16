import sqlite3
from sqlite3 import Error

from flask import Flask, redirect, render_template, request

DATABASE = "zeds_threads.db"

# Create a Flask app
app = Flask(__name__, template_folder='templates')

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


@app.route('/login.html', methods = ['POST', 'GET'])
def login():
  return render_template('login.html')
        
@app.route('/signup.html', methods = ['POST', 'GET'])
def render_signup_page():
  con = create_connection(DATABASE)
  cur = con.cursor()
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
    query = "INSERT INTO user(fname, lname, email, password) VALUES(?, ?, ?, ?)"

    try:
      cur.execute(query, (fname, lname, email, password)) #this line actually executes the query
    except sqlite3.IntegrityError:
      con.close()
      return redirect('/signup?error=Email+is+already+used')

    con.commit()  
    con.close()

    #return redirect("/login")
  return redirect("/login")


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
