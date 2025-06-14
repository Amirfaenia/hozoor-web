
from flask import Flask, render_template, request, redirect, send_file
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_FILE = 'data.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        status TEXT,
                        date TEXT
                    )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    status = request.form['status']
    date = request.form['date']
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO attendance (name, status, date) VALUES (?, ?, ?)", (name, status, date))
        conn.commit()
    return redirect('/')

@app.route('/export')
def export():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM attendance")
        rows = c.fetchall()

    with open("export.csv", "w", encoding="utf-8") as f:
        f.write("ID,Name,Status,Date\n")
        for row in rows:
            f.write(",".join(map(str, row)) + "\n")

    return send_file("export.csv", as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)
