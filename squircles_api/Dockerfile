# pull official base image
FROM python:3.8.12-alpine

ENV PYTHONUNBUFFERED=1
# set work directory
WORKDIR /Users/hoosyong/projects/handbook_api_django/squircles_api
COPY requirements.txt /Users/hoosyong/projects/handbook_api_django/squircles_api
# set environment variables
# install dependencies
RUN \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt && \
 apk --purge del .build-deps

# copy project
COPY . /Users/hoosyong/projects/handbook_api_django/squircles_api
EXPOSE 5000
CMD [ "python", "manage.py", "runserver"]