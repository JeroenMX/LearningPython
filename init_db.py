import sqlite3
import random
from datetime import datetime, timedelta


def getrandomname():
    names = ["Valentina", "Elba", "Jeroen"]
    return names[random.randint(0, len(names)-1)]


def getrandomcount(length):
    result = []

    for i in range(length):
        result.append(random.randint(0, 50))

    return result


def getrandomdate(length):
    result = []

    now = datetime.today()

    for i in range(length):
        now = now - timedelta(days=1)
        result.append(str(now.date()))

    return result


connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

dates = getrandomdate(25)

count = 1
for date in dates:
    postCount = random.randint(1, 10)

    for pc in range(postCount):
        cur.execute("INSERT INTO posts (title, content, created) VALUES (?, ?, ?)",
                    ('Some posted text', 'Content for post', date)
                    )

        postId = cur.lastrowid

        commentCount = random.randint(1, 10)

        for cc in range(commentCount):
            cur.execute("INSERT INTO comments (postId, name, content, created) VALUES (?, ?, ?, ?)",
                        (postId, getrandomname(), 'this is the text for the comment', date)
                        )


connection.commit()
connection.close()