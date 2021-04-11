from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route("/drawing")
def drawing():
    return render_template('drawing.html')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route("/chart")
def chartindex():
    conn = get_db_connection()
    postRows = conn.execute('SELECT COUNT(*) AS PostCount, strftime("%d-%m-%Y", created) AS PostDate FROM posts group by strftime("%d-%m-%Y", created)').fetchall()
    commentRows = conn.execute('SELECT COUNT(*) AS CommentCount, strftime("%d-%m-%Y", created) AS CommentDate FROM comments group by strftime("%d-%m-%Y", created)').fetchall()
    conn.close()

    posts = [dict(row) for row in postRows]
    comments = [dict(row) for row in commentRows]

    jsonData = {"posts": posts, "comments": comments}

    return render_template('chart.html', json=jsonData)


if __name__ == '__main__':
    app.run()


