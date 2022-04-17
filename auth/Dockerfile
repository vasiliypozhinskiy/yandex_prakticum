FROM python:3.8

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY /src /app/

EXPOSE 5000

CMD /wait && gunicorn --worker-class gevent --workers 4 --bind 0.0.0.0:5000 main:app