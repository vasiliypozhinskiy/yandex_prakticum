FROM python:3.8

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

RUN apt-get update && apt-get install nano

WORKDIR /app

COPY requirements.txt /app/
COPY /src /app/
COPY entrypoint_debug.sh /app/
COPY flask_debug.sh /app/
COPY grpc_debug.sh /app/

COPY entrypoint_prod.sh /app/

EXPOSE 5000 50051

RUN pip install -r requirements.txt
RUN ["chmod", "+x", "./entrypoint_debug.sh"]
RUN ["chmod", "+x", "./flask_debug.sh"]
RUN ["chmod", "+x", "./grpc_debug.sh"]

RUN ["chmod", "+x", "./entrypoint_prod.sh"]

CMD  ./entrypoint_prod.sh