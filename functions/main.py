from flask import Flask, request, g, redirect
import sqlite3

app = Flask(__name__)

# Connect to the SQLite database
conn = sqlite3.connect('email_db.sqlite')
cursor = conn.cursor()

# Create the "emails" table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 email TEXT,
                 message TEXT,
                 privacy_policy BOOLEAN
                 )''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Configuration
DATABASE = 'email_db.sqlite'

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Function to close the database connection
@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Handle form submission and insert email into the database
def handle_form_submission(name, email, message, privacy_policy):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO emails (name, email, message, privacy_policy) VALUES (?, ?, ?, ?)", (name, email, message, privacy_policy))
    db.commit()

@app.route('/contact', methods=['POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        privacy_policy = request.form.get('privacy-policy') == 'yes'

        handle_form_submission(name, email, message, privacy_policy)

        return redirect('https://twistedtechnology.net/')

if __name__ == '__main__':
    app.run(debug=True)
