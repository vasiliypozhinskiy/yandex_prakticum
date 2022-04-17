FROM python:3.8

WORKDIR /tests
COPY requirements.txt /tests/
RUN pip install -r requirements.txt
COPY . /tests/

CMD python utils/wait_for_redis.py && python utils/wait_for_es.py && pytest /tests/src/