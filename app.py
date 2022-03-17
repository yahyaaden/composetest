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
    return 'Welcome my friend! To navigate this ugly page press <a href="http://localhost:8000/hit">hit!</a> and <a href="http://localhost:8000/html">html!</a>'

@app.route('/hit')
def hit():
    count = get_hit_count()
    return 'Hey! This page has been {} times.\n'.format(count)

@app.route('/html/')
def html():
    return render_template('generatestub.html')


