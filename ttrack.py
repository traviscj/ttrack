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

def epoch2pacific(value):
    return arrow.get(value).to('US/Pacific')
@app.template_filter('epochformat')
def epochformat(value):
    return epoch2pacific(value).format('YYYY-MM-DD HH:mm:ss')
@app.template_filter('humanize')
def humanize(value):
    return epoch2pacific(value).humanize()

def pre_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(EVENT_SCHEMA)
    return conn, c
def post_db(conn):
    conn.commit()
    conn.close()
def insert(verb, noun):
    conn, c = pre_db()
    timestamp = arrow.utcnow().timestamp
    c.execute("INSERT INTO events (verb, noun, timestamp) VALUES (?, ?, ?);",
        (verb, noun, timestamp))
    post_db(conn)
def get_all():
    conn, c = pre_db()
    result = []
    for row in c.execute('SELECT * FROM events ORDER BY timestamp'):
        result.append(row)
    post_db(conn)
    return result

verbs=["leave", "arrive"]
nouns=["home", "work"]

@app.route("/")
def hello():
    res = get_all()
    return render_template('index.html', res=res, verbs=verbs, nouns=nouns)

@app.route("/mark/<verb>/<noun>")
def mark(verb, noun):
    print "sure, {verb} {noun}".format(verb=verb,noun=noun)
    insert(verb, noun)
    return redirect(url_for('hello'))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
