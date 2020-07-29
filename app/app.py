from typing import Tuple
import socket
import time
import os

from redis import Redis
from flask import Flask


def get_redis() -> Redis:
    redis_url = os.getenv('REDIS_URL', None)
    redis_port = os.getenv('REDIS_PORT', 6379)

    if not redis_url:
        raise Exception('REDIS_URL not passed')

    redis = Redis(host=redis_url, port=redis_port)
    return redis


app = Flask(__name__)
cache = get_redis()


hits = 0

def get_hit_count() -> int:
    global hits
    hits += 1
    return hits


def get_hit_count_with_cache() -> int:
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
def index() -> str:
    return '<h1>Hello World!</h1>'


@app.route('/hits/cache')
def get_hits_cache():
    count = get_hit_count_with_cache()
    hostname = socket.gethostname()
    return f'<h1>Hello World! I have been seen {count} times on {hostname}</h1>'


@app.route('/hits')
def get_hits():
    count = get_hit_count()
    hostname = socket.gethostname()
    return f'<h1>Hello World! I have been seen {count} times on {hostname}</h1>'


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)
