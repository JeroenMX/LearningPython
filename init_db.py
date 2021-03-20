import sqlite3
import random
from datetime import datetime, timedelta

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

postDate = datetime.now()

for i in range(1000):
    delta = random.randint(10, 240)
    postDate = postDate - timedelta(minutes=delta)
    cur.execute("INSERT INTO posts (title, content, created) VALUES (?, ?, ?)",
                ('Post #' + str(i), 'Content for post #' + str(i), postDate)
                )

connection.commit()
connection.close()
