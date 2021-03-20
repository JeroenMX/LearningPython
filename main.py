from flask import Flask, render_template
from datetime import datetime, timedelta
import random

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


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', values={"title": "test"})

@app.route("/chart")
def chartindex():
    datapointcount = 25

    posts = getrandomcount(datapointcount)
    comments = getrandomcount(datapointcount)
    dates = getrandomdate(datapointcount)

    jsonData = {"dates": dates, "posts": posts, "comments": comments}

    return render_template('chart.html', json=jsonData)


if __name__ == '__main__':
    app.run()


