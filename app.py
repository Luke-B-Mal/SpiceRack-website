import sqlite3
import flask
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

#creates a database if it does not already exist in the files.
def init_db():
    conn = sqlite3.connect("user_spices.db")
    c = conn.cursor()
    # Create a table if it doesn't exist
    c.execute('CREATE TABLE IF NOT EXISTS spices (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

init_db()

#allows for the route to the home page to be established.
@app.route("/")
def index():
    return render_template("index.html")

#connects the HTML input to this file
@app.route("/add_spices", methods=['POST'])
def add_spices():
    data = request.form.get('user_spice_add') #pulls the data from the form in the website
    print(f"DEBUG: Received data from website: {data}")

    #parses over the entries in the form and pulls out the individual spices, should isolate regardless of spaces and capitals
    spices = []
    for entry in data.split(','):
        if entry.strip():
            spices.append(entry.lower())
    
    conn = sqlite3.connect("user_spices.db") #connects to the actual database as established previously.
    c = conn.cursor()
    for spice in spices:
        c.execute("INSERT INTO spices (name) VALUES (?)", (spice,))

    conn.commit()
    conn.close()

    return redirect("/") #puts user back on main page.

if __name__ == "__main__":
    app.run(debug=True)
