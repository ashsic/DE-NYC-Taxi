FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY green_taxi_script.py green_taxi_script.py

ENTRYPOINT [ "python", "green_taxi_script.py" ]