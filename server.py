from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '4221289613'

CORS(app)
conn = mysql.connector.connect(user='root',
                              password='user1234',
                              host='localhost',
                              database='library')

@app.route('/')
def home():
  return render_template('home.html', form_action="/signup")

@app.route('/login', methods=['GET','POST'])
def login():
  error = None
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
        session['email'] = email
        return redirect(url_for('data'))
    else:
      error = 'Invalid email or password'

  return render_template('home.html', error=error)

@app.route('/signup', methods=['GET','POST'])
def signup():
  error = None
  if request.method == 'POST':
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
      error = 'Email already in use'
    else:
      cursor = conn.cursor()
      cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
      conn.commit()
      cursor.close()
      return redirect(url_for('login'))
  return jsonify({'success': False, 'error': error})

@app.route('/logout')
def logout():
  # Clear the session data
  session.clear()
  # Redirect the user to the login page
  return redirect(url_for('login'))

@app.route('/data')
def data():
  if session.get('email'):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM users WHERE email=(%s)", (session['email'],))
    user = cursor.fetchone()
    cursor.close()
  else:
    user = None
  if user is not None:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    cursor.close()
    return render_template('data.html',name=user['name'], rows=rows)
  return redirect(url_for('home'))
  

@app.route('/data-fetch')
def data_fetch():
  if session.get('email'):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM users WHERE email=(%s)", (session['email'],))
    user = cursor.fetchone()
    cursor.close()
  else:
    user = None
  if user is not None:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)
  return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_data():
  cursor = conn.cursor(dictionary=True)
  data = request.get_json()
  id = data['id']
  book = data['book']
  author = data['author']
  isbn = data['isbn']
  description = data['description']
  cursor.execute("INSERT INTO books (ID, Books, Author, ISBN, Description) VALUES (%s, %s, %s, %s, %s)", (id, book, author, isbn, description))
  conn.commit()
  cursor.close()
  # Create a URL for the book using the unique ID
  # Redirect the user to the URL for the book
  return jsonify({'success': True})

@app.route('/book/<book_id>')
def book(book_id):
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT * FROM books WHERE ID=%s", (book_id,))
  books = cursor.fetchone()
  cursor.close()
  return render_template('book.html', books=books)


if __name__ == '__main__':
    app.run()
