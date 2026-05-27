from flask import Flask, render_template, request, redirect
import sqlite3

# Flask automatically looks for "templates" and "static" folders!
app = Flask(__name__)

# Database connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
)
""")
conn.commit()

# Home page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Register user
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )
    conn.commit()
    return redirect("/")

# Admin dashboard
@app.route("/admin", methods=["GET"])
def admin():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("admin.html", users=users)

# Delete user
@app.route("/delete/<int:user_id>", methods=["GET"])
def delete_user(user_id):
    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )
    conn.commit()
    return redirect("/admin")

# Run server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
