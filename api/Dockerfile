FROM python:3.8

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY /src /app/
COPY prod_ep.sh/ /app/
RUN ["chmod", "+x", "prod_ep.sh"]

EXPOSE 8000

CMD ./prod_ep.sh