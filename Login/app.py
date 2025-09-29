from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------- DB Setup ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER,
            weight REAL,
            height REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        flash("Signup successful! Please log in.", "success")
    except sqlite3.IntegrityError:
        flash("Username already exists. Try a different one.", "error")
    finally:
        conn.close()

    return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session["username"] = username
        return redirect(url_for("user_home"))
    else:
        flash("Invalid username or password.", "error")
        return redirect(url_for("home"))

@app.route("/home", methods=["GET", "POST"])
def user_home():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        age = request.form.get("age")
        weight = request.form.get("weight")
        height = request.form.get("height")
        cursor.execute("UPDATE users SET age=?, weight=?, height=? WHERE username=?", (age, weight, height, username))
        conn.commit()

    cursor.execute("SELECT username, age, weight, height FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    return render_template("home.html", user=user_data)

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
