from flask import jsonify

from app.core import app
from app.models.test_models import Test

from app.db.redis import get_redis


@app.route('/auth/test')
def test():
    return jsonify({'result': 'ok'})


@app.route('/auth/db_test')
def db_test():
    test_texts = Test.query.all()
    result = [text.testfield for text in test_texts]
    return jsonify({'result': result})


@app.route('/auth/redis_test')
def redis_test():
    with get_redis() as redis:
        redis.set('key', 'Hello from redis')
        result = redis.get('key').decode('utf-8')
        return jsonify({'result': result})
