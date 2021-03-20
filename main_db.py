import sqlite3
from flask import Flask
from flask import render_template
import random
import statistics

def getrandomcommentcount(length):
    result = []

    for i in range(length):
        result.append(random.randint(0, 50))

    return result


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route("/chart")
def chartindex():
    conn = get_db_connection()
    data = conn.execute('SELECT COUNT(*) AS PostCount, strftime("%d-%m-%Y", created) AS PostDate FROM posts group by strftime("%d-%m-%Y", created)').fetchall()
    conn.close()

    posts = [dict(row) for row in data]
    comments = getrandomcommentcount(len(posts))
    average = int(statistics.mean(int(row[0]) for row in data))

    jsonData = {"posts": posts, "comments": comments, "average": average}

    return render_template('chart.html', json=jsonData)


if __name__ == '__main__':
    app.run()


