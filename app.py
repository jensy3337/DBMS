from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="ecommerce_db"
)

@app.route('/')
def home():
    search = request.args.get('search')
    sort = request.args.get('sort')

    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM Products"

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
    app.run(debug=True)
