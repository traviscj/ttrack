from flask import Flask, render_template, redirect, url_for
import arrow
import sqlite3
app = Flask(__name__)

# small personal data monitoring app
# 
# - selector for leaving
# - button for arrived
#
# Will naturally need to
#  $ pip install flask arrow sqlite3

def insert(noun, verb):
    conn = sqlite3.connect('ttrack.db')
    timestamp = arrow.utcnow().timestamp
    c = conn.cursor()
    c.execute("INSERT INTO events (noun, verb, timestamp) VALUES (?, ?, ?);",
        (noun, verb, timestamp))
    conn.commit()
    conn.close()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/mark/<verb>/<noun>")
def mark(verb, noun):
    print "sure, {verb} {noun}".format(verb=verb,noun=noun)
    insert(noun, verb)
    return redirect(url_for('hello'))

# database
# schema: CREATE TABLE events (id INTEGER PRIMARY KEY, noun TEXT, verb TEXT, timestamp INTEGER);


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
