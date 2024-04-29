FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y build-essential default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
apt-get install -y supervisor && \
mkdir -p /var/log/supervisor

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY UI ./UI
COPY API ./API

EXPOSE 5005 5000

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient -lpthread -lz -lm -lrt -latomic -lssl -lcrypto"


CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]




