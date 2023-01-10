from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
from flask_cors import CORS
from datetime import timedelta
from datetime import date

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
    email = request.json['email']
    password = request.json['password']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    if user is not None:
        session['email'] = email
        return jsonify({'success':True})
    else:
      error = 'Invalid email or password'
    return jsonify({'success':False,'error':error})

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
      session['email'] = email
      return jsonify({'success': True,})
  return jsonify({'success': False, 'error': error})

@app.route('/logout')
def logout():
  # Clear the session data
  session.clear()
  # Redirect the user to the login page
  return redirect(url_for('home'))

@app.route('/data')
def data():
  if session.get('email'):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM users WHERE email=(%s)", (session['email'],))
    user = cursor.fetchone()
    cursor.close()
  else:
    user = None
  if user:
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    cursor.close()
    return render_template('data.html',name=user['name'], rows=rows)
  return redirect(url_for('home'))
  

@app.route('/data-fetch')
def data_fetch():
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT * FROM books")
  rows = cursor.fetchall()
  cursor.close()
  return jsonify(rows)

@app.route('/data-fetch-management')
def data_fetch_manage():
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT * FROM books ORDER BY ID DESC LIMIT 10;")
  rows = cursor.fetchall()
  cursor.close()
  return jsonify(rows)

@app.route('/add', methods=['POST'])
def add_data():
  cursor = conn.cursor(dictionary=True)
  data = request.get_json()
  book = data['book']
  author = data['author']
  isbn = data['isbn']
  description = data['description']
  cursor.execute("INSERT INTO books ( Books, Author, ISBN, Description) VALUES ( %s, %s, %s, %s)", ( book, author, isbn, description))
  conn.commit()
  cursor.close()
  return jsonify({'success': True})

@app.route('/delete', methods=['POST'])
def delete_data():
  cursor = conn.cursor(dictionary=True)
  data = request.get_json()
  book = data['book']
  cursor.execute("DELETE FROM books WHERE Books=(%s)", (book,))
  conn.commit()
  cursor.close()
  return jsonify({'success': True})

@app.route('/update', methods=['POST'])
def update_data():
  cursor = conn.cursor(dictionary=True)
  data = request.get_json()
  book = data['book']
  cursor.execute("SELECT * FROM books WHERE Books=%s", (book,))
  value = cursor.fetchone()
  if value:
    author = data['author']
    if author:
      cursor.execute("UPDATE books SET Author =(%s) WHERE Books=(%s)", (author,book))
      conn.commit()
    isbn = data['isbn']
    if isbn:
      cursor.execute("UPDATE books SET ISBN =(%s) WHERE Books=(%s)", (isbn,book))
      conn.commit()
    desc = data['desc']
    if desc:
      cursor.execute("UPDATE books SET Description =(%s) WHERE Books=(%s)", (desc,book))
      conn.commit()
    cursor.close()
    return jsonify({'success': True})
  return jsonify({'success': False})

@app.route('/book/<book_id>')
def book(book_id):
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT * FROM books WHERE ID=%s", (book_id,))
  books = cursor.fetchone()
  cursor.close()
  return render_template('book.html', books=books)

@app.route('/book')
def books():
  return render_template('books.html')

@app.route('/lend')
def lend():
  if session.get('email'):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM users WHERE email=(%s)", (session['email'],))
    user = cursor.fetchone()
    cursor.close()
  else:
    user = None
  if user:
    return render_template('lend.html')
  return redirect(url_for("login"))

@app.route('/lend-add', methods=['POST'])
def lend_add():
  cursor = conn.cursor(dictionary=True)
  data = request.get_json()
  name = data['name']
  book = data['book']
  today = date.today()
  duedate = today + timedelta(days=15)
  cardnumber = data['cardnumber']
  cursor.execute("INSERT INTO lending ( Name, Book, Date, Due_Date, cardnumber) VALUES ( %s, %s, %s, %s, %s)", ( name,book, today, duedate, cardnumber))
  conn.commit()
  cursor.close()
  return jsonify({'success': True})

@app.route('/lend-fetch')
def lend_fetch():
  cursor = conn.cursor(dictionary=True)
  cursor.execute("SELECT * FROM lending")
  rows = cursor.fetchall()
  cursor.close()
  return jsonify(rows)

@app.route('/search', methods=['POST'])
def search():
  cursor = conn.cursor(dictionary=True)
  data = request.get_json()
  search_term = data['search_term']
  query = "SELECT * FROM books WHERE Books=%s OR Author=%s OR ISBN=%s;"
  cursor.execute(query, (search_term, search_term, search_term))
  rows = cursor.fetchall()
  cursor.close()
  if rows:
    return jsonify({'success': True, 'rows':rows})
  return jsonify({'success': False})

if __name__ == '__main__':
    app.run()
