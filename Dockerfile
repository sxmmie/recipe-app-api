FROM python:3.7-alpine
LABEL maintainer="samuelumohjnr@gmail.com"

# Environment var (PYTHONUNBUFFERED mode)
ENV PYTHONUNBUFFERED 1

# dependencies
COPY ./requirement.txt /requirement.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirement.txt
RUN apk del .tmp-build-deps

# make a directory inside docker image to store application source
RUN mkdir /app
WORKDIR /app
COPY /app /app

# create a user to run app using docker
RUN adduser -D user
USER user