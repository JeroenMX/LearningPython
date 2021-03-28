from flask import Flask, render_template
from datetime import datetime, timedelta
import random
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', values={"title": "test"})


@app.route("/drawing")
def drawing():
    return render_template('drawing.html')


@app.route("/chart")
def chartindex():
    conn = get_db_connection()
    postRows = conn.execute('SELECT COUNT(*) AS PostCount, strftime("%d-%m-%Y", created) AS PostDate FROM posts group by strftime("%d-%m-%Y", created)').fetchall()
    commentRows = conn.execute('SELECT COUNT(*) AS CommentCount, strftime("%d-%m-%Y", created) AS CommentDate FROM comments group by strftime("%d-%m-%Y", created)').fetchall()
    conn.close()

    posts = [dict(row) for row in postRows]
    comments = [dict(row) for row in commentRows]
    #dates = list(set(posts["PostDate"]) | set("CommentDate"))

    jsonData = {"posts": posts, "comments": comments}

    return render_template('chart.html', json=jsonData)


if __name__ == '__main__':
    app.run()


