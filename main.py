from flask import Flask, render_template, redirect, request
import sqlite3
from sqlite3 import Error
from flask_bcrypt import Bcrypt
from flask import session

# Create a Flask app
app = Flask(__name__, template_folder='templates')
bcrypt = Bcrypt(app)
app.secret_key = "wegc1234"
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
      
@app.route('/outerwear.html')
def render_outerwear():
    con = create_connection(DATABASE)
    if con:
        query = "SELECT name, main_colours, price FROM clothing_data WHERE cat_id = 1"
        cur = con.cursor()
        cur.execute(query)
        clothing_list = cur.fetchall()
        con.close()

        if clothing_list:
            return render_template('outerwear.html', clothing=clothing_list)
        else:
            return render_template('outerwear.html', clothing=[], message="No outerwear items found.")
    else:
        return "Error"
      
@app.route('/tops.html')
def render_tops():
    con = create_connection(DATABASE)
    if con:
        query = "SELECT name, main_colours, price FROM clothing_data WHERE cat_id = 4"
        cur = con.cursor()
        cur.execute(query)
        clothing_list = cur.fetchall()
        con.close()

        if clothing_list:
            return render_template('tops.html', clothing=clothing_list)
        else:
            return render_template('tops.html', clothing=[], message="No top items found.")
    else:
        return "Error"

@app.route('/dresses.html')
def render_dresses():
    con = create_connection(DATABASE)
    if con:
        query = "SELECT name, main_colours, price FROM clothing_data WHERE cat_id = 2"
        cur = con.cursor()
        cur.execute(query)
        clothing_list = cur.fetchall()
        con.close()

        if clothing_list:
            return render_template('dresses.html', clothing=clothing_list)
        else:
            return render_template('dresses.html', clothing=[], message="No dresses found.")
    else:
        return "Error"
      
@app.route('/footwear.html')
def render_footwear():
    con = create_connection(DATABASE)
    if con:
        query = "SELECT name, main_colours, price FROM clothing_data WHERE cat_id = 3"
        cur = con.cursor()
        cur.execute(query)
        clothing_list = cur.fetchall()
        con.close()

        if clothing_list:
            return render_template('footwear.html', clothing=clothing_list)
        else:
            return render_template('footwear.html', clothing=[], message="No footwear items found.")
    else:
        return "Error"
      
@app.route('/bottoms.html')
def render_bottoms():
    con = create_connection(DATABASE)
    if con:
        query = "SELECT name, main_colours, price FROM clothing_data WHERE cat_id = 5"
        cur = con.cursor()
        cur.execute(query)
        clothing_list = cur.fetchall()
        con.close()

        if clothing_list:
            return render_template('bottoms.html', clothing=clothing_list)
        else:
            return render_template('bottoms.html', clothing=[], message="No bottoms found.")
    else:
        return "Error"
      
@app.route('/acessories.html')
def render_acessories():
    con = create_connection(DATABASE)
    if con:
        query = "SELECT name, main_colours, price FROM clothing_data WHERE cat_id = 6"
        cur = con.cursor()
        cur.execute(query)
        clothing_list = cur.fetchall()
        con.close()

        if clothing_list:
            return render_template('acessories.html', clothing=clothing_list)
        else:
            return render_template('acessories.html', clothing=[], message="No acessories found.")
    else:
        return "Error"
@app.route('/login.html', methods=['POST', 'GET'])
def render_login_page():
    con = create_connection(DATABASE)
    if con:
        if is_logged_in():
            first_name = session.get('firstname', 'User')
            return redirect(f'/welcome?name={first_name}')  # Redirect to welcome page

        if request.method == 'POST':
            email = request.form['email'].strip().lower()
            password = request.form['password'].strip()

            query = "SELECT id, first_name, password FROM user WHERE email =?"
            cur = con.cursor()
            cur.execute(query, (email,))
            user_data = cur.fetchone()

            con.close()

            if user_data is None:
                return redirect("/login.html?error=Email+invalid+or+password+incorrect")

            try:
                user_id = user_data[0]
                first_name = user_data[1]
                db_password = user_data[2]
            except IndexError:
                return redirect("/login.html?error=Email+invalid+or+password+incorrect")

            if not bcrypt.check_password_hash(db_password, password):
                return redirect("/login.html?error=Email+invalid+or+password+incorrect")

            session['email'] = email
            session['user_id'] = user_id
            session['firstname'] = first_name

            return redirect(f'/welcome?name={first_name}')  # Redirect to welcome page

        error = request.args.get('error')
        return render_template('login.html', logged_in=is_logged_in(), error=error)
    else:
        return "Error connecting to the database."

#chat gpt assisted me with this idea of a welcome page
@app.route('/welcome')
def welcome():
    first_name = request.args.get('name', 'Guest')  # Get the first name from query parameters
    return render_template('welcome.html', name=first_name)



@app.route('/logout') #logout function
def logout():
  print(list(session.keys()))
  [session.pop(key) for key in list(session.keys())]
  print(list(session.keys()))
  return render_template('login.html')
  


@app.route('/signup', methods = ['POST', 'GET'])
def render_signup_page():
  con = create_connection(DATABASE)
  if con:
    if request.method == 'POST':
      fname = request.form.get('fname')  
      lname = request.form.get('lname')  
      email = request.form.get('email')
      password = request.form.get('password')
      password2 = request.form.get('password2')
  
      hashed_password = bcrypt.generate_password_hash(password)  #creating a hash password
      print(hashed_password)  
      
      query = "INSERT INTO user(first_name, last_name, email, password) VALUES(?, ?, ?, ?)"
      cur = con.cursor()
  
      try:
        cur.execute(query, (fname, lname, email, hashed_password)) #this line actually executes the query
      except sqlite3.IntegrityError:
        con.close()
        return redirect('/signup?error=Email+is+already+used')
  
      con.commit()  
      con.close()
  
      return redirect("/login.html")
    return render_template('signup.html')
  else:
    return "Error"

def is_logged_in():
  if session.get("email") is None:
    print("not logged in")
    return False
  else:
    print("logged in")
    return True
    
#admin section
@app.route('/admin')
def render_admin():
  if not is_logged_in():
    return redirect('/message=Need+to+be+logged+in.')
  con = create_connection(DATABASE)
  if con:
    #fetch the categories
    query = "SELECT * FROM clothing_category"
    cur = con.cursor()
    cur.execute(query)
    category_list = cur.fetchall()

    #fetch the products
    query = "SELECT * FROM clothing_data"
    cur.execute(query)
    product_list = cur.fetchall()
    print(product_list)

    con.close()

    if not product_list:
      return render_template("admin.html", logged_in=is_logged_in(), categories=category_list, no_items=True)
    return render_template("admin.html", logged_in=is_logged_in(), categories=category_list, products=product_list)


#adding a category function
@app.route('/add_category', methods = ['POST'])
def add_category():
  if not is_logged_in():
    return redirect('/message=Need+to+be+logged+in.')
  if request.method == "POST":
    print(request.form)
    cat_name = request.form.get('name')
    print(cat_name)
    con = create_connection(DATABASE)
    if con:
      query = "INSERT INTO clothing_category (name) VALUES (?)"
      cur = con.cursor()
      cur.execute(query, (cat_name, ))
      con.commit()
      con.close()
    return redirect('/admin')


#deleting a category function
@app.route('/delete_category', methods = ['POST'])
def render_delete_category():
  if not is_logged_in():
    return redirect('/message=Need+to+be+logged+in.')

  if request.method == "POST":
    con = create_connection(DATABASE)
    if con:
      category = request.form.get('cat_id')
      print(category)
      category = category.split(", ")
      cat_id = category[0]
      cat_name = category[1]
      return render_template("delete_confirm.html", id=cat_id, name=cat_name, type='category')
    return redirect("/admin")

#confirmation of delete category
@app.route('/delete_category_confirm/<int:cat_id>')
def render_delete_category_confirm(cat_id):
  if not is_logged_in():
    return redirect('/message=Need+to+be+logged+in.')
  con = create_connection(DATABASE)
  if con:
    query = "DELETE FROM clothing_category WHERE id = ?"
    cur = con.cursor()
    cur.execute(query, (cat_id, ))
    con.commit()
    con.close()
    return redirect("/admin")

#adding an item 
@app.route('/add_item', methods = ['POST'])
def render_add_item():
  con = create_connection(DATABASE)
  if con:
    if not is_logged_in():
      return redirect('/message=Need+to+be+logged+in.')
    if request.method == "POST":
      print(request.form)
      item_name = request.form.get('name')
      item_colours = request.form.get('main_colours')
      item_price = request.form.get('price')

      print(item_name, item_colours, item_price)
      query = "INSERT INTO clothing_data (name, main_colours, price) VALUES (?, ?, ?)"
      cur = con.cursor()
      cur.execute(query, (item_name, item_colours, item_price))
      con.commit()
      con.close()
    return redirect('/admin')


#deleting a item function
@app.route('/delete_item', methods=['POST'])
def render_delete_item():
  if not is_logged_in():
    return redirect('/message=Need+to+be+logged+in.')

  if request.method == "POST":
    con=create_connection(DATABASE)
    products = request.form.get('clothing_id')
    print(products)
    if products is None:
      return redirect("/admin?error=No+item+selected")

    products = products.split(", ")
    item_id = products[0]
    item_name = products[1] if len(products) > 1 else "" #assign an empty string if item_name doesn't exist
    print(item_id, item_name)

    return render_template("delete_item_confirm.html", id=item_id, name=item_name, type='products')
  return redirect("/admin")

#confirm delete item
@app.route('/delete_item_confirm/<int:item_id>')
def render_delete_item_confirm(item_id):
  print("I am in here")
  if not is_logged_in():
    return redirect('/message=Need+to+be+logged+in.')

  con=create_connection(DATABASE)
  if con:
    query = "DELETE FROM clothing_data WHERE id = ?"
    cur = con.cursor()
    cur.execute(query, (item_id, ))
    con.commit()
    print("Test: ", item_id)
    con.close()  

  return redirect("/admin")
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
