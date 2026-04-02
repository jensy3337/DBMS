from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    stock_qty INTEGER,
    category TEXT
)
""")

# INSERT DATA IF EMPTY
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
    search = request.args.get('search')
    sort = request.args.get('sort')
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    query = "SELECT name, price, stock_qty, category FROM Products WHERE 1=1"

    if search:
        query += f" AND name LIKE '%{search}%'"

    if category:
        query += f" AND category='{category}'"

    if min_price and max_price:
        query += f" AND price BETWEEN {min_price} AND {max_price}"

    if sort == "low":
        query += " ORDER BY price ASC"
    elif sort == "high":
        query += " ORDER BY price DESC"
    elif sort == "name":
        query += " ORDER BY name ASC"

    cursor.execute(query)
    products = cursor.fetchall()

    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
