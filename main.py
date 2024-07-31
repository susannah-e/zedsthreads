from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

DATABASE = "zeds_threads.db"

# Create a flask app
app = Flask(
  __name__,
  template_folder='templates',

)
def create_connection(zeds_threads):
  try:
    connection = sqlite3.connect(zeds_threads)
    return connection
  except Error as e:
    print(e)
  return None


# Index page (now using the index.html file)
@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  # Run the Flask app
  app.run(
  host='0.0.0.0',
  debug=True,
  port=8080
  )
