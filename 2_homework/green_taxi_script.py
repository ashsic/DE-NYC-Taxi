import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    url = params.url
    table_name = params.table_name

    csv_name = 'output.csv'

    # WINDOWS:
    # os.system(f"C:\\Users\\Ashton\\github_Repos\\DE-NYC-Taxi\\wget.exe {url} -O {csv_name}.gz")
    # os.system(f"gzip -d {csv_name}.gz")

    # UBUNTU:
    os.system(f"wget {url} -O {csv_name}.gz")
    os.system(f"gzip -d {csv_name}.gz")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    os.system(f"wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv -O zone_map.csv")
    zone = pd.read_csv('zone_map.csv')
    zone.to_sql(name='zone_map', con=engine, if_exists='replace')


    print('starting')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        start = time()
        df = next(df_iter)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        end = time()
        print('inserted chunk in seconds:', end - start)
        if len(df) < 100000:
            print('all done!')
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of table we will write results to in postgres')
    parser.add_argument('--url', help='url of the csv file')
    args = parser.parse_args()

    main(args)