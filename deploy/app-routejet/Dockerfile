FROM nginx:1.23.1

RUN apt-get update -y
RUN apt-get install python3.10.1 -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

RUN rm -f /app/routejet/celerybeat.pid

EXPOSE 80

CMD ["sh", "launch.sh"]
