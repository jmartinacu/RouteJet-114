FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /routejet

RUN pip install --upgrade pip

COPY requirements.txt /routejet/
RUN pip install -r requirements.txt

COPY . /routejet/

RUN python routejet/manage.py loaddata product.json