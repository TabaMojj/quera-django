FROM python:3.8

WORKDIR /app/codecup/

RUN apt update && apt install -y vim curl gettext

COPY requirements.txt /app/codecup
ENV PIP_NO_CACHE_DIR 1
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

COPY . .
