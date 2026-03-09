FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt /temp/requirements.txt
WORKDIR /app
COPY . /app

RUN pip install -r /temp/requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "leet_code.wsgi:application", "--bind", "0.0.0.0:8000"]