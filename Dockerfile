from alpine:3.7

WORKDIR /app
ADD . /app

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
Run pip3 --no-cache-dir install -r requirements.txt
