import os
import argparse

import pandas as pd

from sqlalchemy import create_engine

def main(params):
    username = params.user
    password = params.password
    host = params.host
    port = params.port
    table_name = params.table
    db = params.db
    url = params.url
    csv_name = 'output.csv'

    os.system(f'wget {url} -O {csv_name}.gz')
    os.system(f'gunzip {csv_name}.gz')

    df = pd.read_csv(csv_name, nrows=100)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db}')
    engine.connect()

    pd.io.sql.get_schema(df, name=table_name, con=engine)

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    print('inserting first chunk')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while len(df) == 100000:
        print("inserting another chunk...")
        
        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')

        print("chunk inserted.")
        print(pd.read_sql("SELECT COUNT(*) FROM taxi;", con=engine))
        

    print('script over')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db name for postgres')
    parser.add_argument('--table', help='table name for postgres')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
