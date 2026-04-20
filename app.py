from flask import Flask, request, redirect, render_template, jsonify
import sqlite3

app = Flask(__name__)

#creates the spice database if it does not already exist in the directory.
def init_s_db():
    conn = sqlite3.connect("data/user_spices.db")
    c = conn.cursor()
    # Create a table if it doesn't exist
    c.execute('CREATE TABLE IF NOT EXISTS spices (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

init_s_db()

#creates the recipe database if it does not already exist in the directory.
def init_r_db():
    conn = sqlite3.connect("data/user_recipes.db")
    c = conn.cursor()
    # Create a table if it doesn't exist
    c.execute('CREATE TABLE IF NOT EXISTS recipes (title TEXT, category TEXT)')
    conn.commit()
    conn.close()

init_r_db()

#allows for the route to the home page to be established. Also pushes the 
@app.route("/")
def index():
    #queries the user spice database for the names of the spices currently in the database. If none [...]
    conn_s = sqlite3.connect("data/user_spices.db")
    c_s = conn_s.cursor()
    c_s.execute("SELECT name FROM spices")
    spice_names_messy = c_s.fetchall()
    conn_s.close()

    #acutally creates the list of spices from the SQL query before
    user_spices = []
    for spice_name in spice_names_messy:
        user_spices.append(spice_name[0])

    #splits the spices list into two parts where the left side will be the "favorites" column (required spices) later in production.
    mid = len(user_spices) // 2 + (len(user_spices) % 2)
    left_spice = user_spices[:mid]
    right_spice = user_spices[mid:]

    #again, queries the user recipe database for the names of the recipes as well as the spices that the recipe uses that the user owns.
    conn_r = sqlite3.connect("data/user_recipes.db")
    c_r = conn_r.cursor()
    c_r.execute("SELECT title, category FROM recipes")
    recipe_rows = c_r.fetchall()
    conn_r.close()

    #creates a list of dictionaries for every observation of the database.
    recipe = []
    for obs in recipe_rows:
        recipe.append({
            "title": obs[0],
            "category": obs[1]
        })

    return render_template("index.html", left_spices = left_spice, right_spices = right_spice, recipes = recipe)

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
    
    conn = sqlite3.connect("data/user_spices.db") #connects to the actual database as established previously.
    c = conn.cursor()
    for spice in spices:
        c.execute("INSERT INTO spices (name) VALUES (?)", (spice,))

    conn.commit()
    conn.close()

    return redirect("/") #puts user back on main page.

@app.route('/get_recipe_details/<title>')
def get_recipe_details(title):
    conn = sqlite3.connect("data/all_recipes.db")
    c = conn.cursor()

    c.execute("SELECT ingredients, directions, image_url FROM recipes WHERE title = ?", (title,))
    result = c.fetchone()
    conn.close()

    if result:

        print(f"DEBUG Image URL for '{title}': '{result[2]}'")

        return jsonify({
            "ingredients": result[0].split(","),
            "directions": result[1].split(","),
            "image": result[2]
        })
    return(jsonify({"error": "Recipe not found"}), 404)

if __name__ == "__main__":
    app.run(debug=True)