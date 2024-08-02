from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

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

@app.route('/database.html')
def render_database():
    con = create_connection(DATABASE)
    if con:
        query = "SELECT name, main_colours, price, clothing_catergory FROM clothing_data"
        cur = con.cursor()
        cur.execute(query)
        clothing_list = cur.fetchall()
        con.close()
        print(clothing_list)
        for clothing in clothing_list:
            print(clothing[3])
            print(clothing)
        return render_template('database.html', clothing=clothing_list)
    else:
        return "Error"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
