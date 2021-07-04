from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
from flask_socketio import SocketIO


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
sio = SocketIO(app)


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route("/drawing")
def drawing():
    return render_template('drawing.html')


@app.route("/chat")
def chat():
    return render_template('chat.html')


@app.route("/tracking")
def tracking():
    return render_template('tracking.html')


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


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            flash('updated!', 'success')
            return redirect(url_for('post', post_id=post['id']))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']), 'danger')
    return redirect(url_for('index'))


@app.route("/chart")
def chartindex():
    conn = get_db_connection()
    postRows = conn.execute(
        'SELECT COUNT(*) AS PostCount, strftime("%d-%m-%Y", created) AS PostDate FROM posts group by strftime("%d-%m-%Y", created)').fetchall()
    commentRows = conn.execute(
        'SELECT COUNT(*) AS CommentCount, strftime("%d-%m-%Y", created) AS CommentDate FROM comments group by strftime("%d-%m-%Y", created)').fetchall()
    conn.close()

    posts = [dict(row) for row in postRows]
    comments = [dict(row) for row in commentRows]

    jsonData = {"posts": posts, "comments": comments}

    return render_template('chart.html', json=jsonData)


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@sio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    sio.emit('my response', json, callback=messageReceived)


clients = {}


@sio.on('mouse_position')
def handle_mouse_position(data):
    print('received mouse position: ' + str(data) + ' sid:' + request.sid)
    clients[request.sid]["data"] = data
    sio.emit('all_coords', clients)


@sio.on('connectUser')
def handle_connect_user(data):
    clients[request.sid] = {"userName": data.get('userName'), "data": {}}
    print('connectUser: ' + str(data) + ' sid:' + request.sid)


@sio.event
def disconnect():
    print('disconnected sid:' + request.sid)
    del clients[request.sid]


@sio.event
def connect():
    print('connected sid:' + request.sid)


if __name__ == '__main__':
    sio.run(app, debug=True)