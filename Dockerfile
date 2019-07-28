FROM python:3.7-alpine
LABEL maintainer="samuelumohjnr@gmail.com"

# Environment var (PYTHONUNBUFFERED mode)
ENV PYTHONUNBUFFERED 1

# dependencies
COPY ./requirement.txt /requirement.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirement.txt
RUN apk del .tmp-build-deps

# make a directory inside docker image to store application source
RUN mkdir /app
WORKDIR /app
COPY /app /app

# All shared media files between different containers are stored here
RUN mkdir -p /vol/web/media
# static files
RUN mkdir -p /vol/web/static
# create a user to run app using docker
RUN adduser -D user
# set the ownership of the dir /vol/web/static to the custom user so it can view/access the user
RUN chown -R user:user /vol/
# add permissions, user can do anything
RUN chmod -R 755 /vol/web
USER user
