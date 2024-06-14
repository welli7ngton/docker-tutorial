import time

import redis
from flask import Flask
import redis.exceptions


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
    count = get_hit_count()

    _msg = f"Hello world! I have been seen {count} times aaaaaaanbbbbbb"

    _css = "<style>body{background-color:yellow}<style/>"

    return _msg + _css
