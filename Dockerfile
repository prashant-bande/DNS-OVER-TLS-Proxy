FROM python:3.6.5-alpine
RUN apk update && apk upgrade && rm -rf /var/cache/apk/*
WORKDIR /usr/src/app
COPY ./app.py .
ENTRYPOINT [ "python", "./app.py" ]