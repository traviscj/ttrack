from flask import Flask, render_template, redirect, url_for
import arrow
import sqlite3
app = Flask(__name__)

# small personal data monitoring app
# 
# - buttons for leaving or arriving home or work
# - those are hooked up to a sqlite3 database
#
# Will naturally need to
#  $ pip install flask arrow sqlite3
#
# TODO some kind of event matching logic.
# TODO table of "unmatched events"


DATABASE_FILE = 'ttrack.db'
EVENT_SCHEMA = """CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, verb TEXT, noun TEXT, timestamp INTEGER)"""

def insert(verb, noun):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(EVENT_SCHEMA)
    
    timestamp = arrow.utcnow().timestamp
    c = conn.cursor()
    c.execute("INSERT INTO events (verb, noun, timestamp) VALUES (?, ?, ?);",
        (verb, noun, timestamp))
    conn.commit()
    conn.close()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/mark/<verb>/<noun>")
def mark(verb, noun):
    print "sure, {verb} {noun}".format(verb=verb,noun=noun)
    insert(verb, noun)
    return redirect(url_for('hello'))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
