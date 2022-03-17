import time

import redis
from flask import Flask, render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    return '<b>Welcome my friend! To navigate this ugly page press <a href="/hit">HIT!</a> and <a href="/html">HTML!</a></b>'

@app.route('/hit')
def hit():
    count = get_hit_count()
    return '<b>Hey! This page has been seen {} times.</b>\n'.format(count)

@app.route('/html/')
@app.route('/html/<name>')
def html(name = None):
    return render_template('generatestub.html', name = name)


