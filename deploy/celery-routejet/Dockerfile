FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

RUN rm -f /app/routejet/celerybeat.pid

WORKDIR /app/routejet

EXPOSE 5432
EXPOSE 6379

ENTRYPOINT ["celery", "-A", "routejet", "worker", "--beat"]

