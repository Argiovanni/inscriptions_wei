FROM python:3.9-alpine

WORKDIR /app

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mysqlclient
RUN python manage.py collectstatic --noinput

RUN apk del build-deps

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
