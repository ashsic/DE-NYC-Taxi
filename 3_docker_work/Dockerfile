FROM python:3.9

RUN apt-get install wget
RUN pip install pandas psycopg2 sqlalchemy

WORKDIR /app
COPY new_pipeline.py new_pipeline.py

ENTRYPOINT [ "python", "new_pipeline.py" ]
