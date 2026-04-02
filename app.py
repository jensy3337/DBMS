from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# PRODUCTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    stock_qty INTEGER,
    category TEXT
)
""")

# ORDERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    customer_name TEXT,
    age INTEGER,
    phone TEXT,
    address TEXT,
    quantity INTEGER
)
""")

# INSERT SAMPLE PRODUCTS
cursor.execute("SELECT COUNT(*) FROM Products")
if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO Products (name, price, stock_qty, category)
    VALUES (?, ?, ?, ?)
    """, [
        ("Laptop", 55000, 10, "Electronics"),
        ("Phone", 20000, 20, "Electronics"),
        ("Headphones", 1500, 50, "Accessories"),
        ("Shoes", 3000, 25, "Fashion"),
        ("Backpack", 1200, 40, "Accessories")
    ])
    conn.commit()


@app.route('/')
def home():
    cursor.execute("SELECT name, price, stock_qty, category FROM Products")
    products = cursor.fetchall()
    return render_template('index.html', products=products)


# 🛒 BUY PAGE
@app.route('/buy/<name>')
def buy(name):
    cursor.execute("SELECT name, price FROM Products WHERE name=?", (name,))
    product = cursor.fetchone()
    return render_template('buy.html', product=product)


# 📥 PLACE ORDER
@app.route('/place_order', methods=['POST'])
def place_order():
    product = request.form['product']
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    address = request.form['address']
    quantity = request.form['quantity']

    cursor.execute("""
    INSERT INTO Orders (product_name, customer_name, age, phone, address, quantity)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (product, name, age, phone, address, quantity))

    conn.commit()

    return render_template('success.html', name=name)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
