FROM python:3.9-alpine

WORKDIR /app

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
