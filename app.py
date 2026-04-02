from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()




@app.route('/')
def home():
    search = request.args.get('search')
    sort = request.args.get('sort')

    query = "SELECT name, price, stock_qty FROM Products"

    if search:
        query += f" WHERE name LIKE '%{search}%'"

    if sort == "low":
        query += " ORDER BY price ASC"
    elif sort == "high":
        query += " ORDER BY price DESC"

    cursor.execute(query)
    products = cursor.fetchall()

    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
