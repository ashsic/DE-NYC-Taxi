
import argparse
import os

from time import time

import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'test.csv'

    # not yet able to get the file download to work correctly. perhaps if the
    # file was unzipped (as in the video) it would be possible

    # windows:
    # os.system(f"/c/Users/Ashton/github_Repos/DE-pipeline-NYTaxi/wget.exe {url} -O {csv_name}.gz")
    # os.system(f"gzip -d {csv_name}.gz")

    # ubuntu:
    os.system(f"wget {url} -O {csv_name}.gz")
    os.system(f"gzip -d {csv_name}.gz")

    print("Done wget and gunzip")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print("engine created")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    print("inserting chunks")

    while True:
        t_start = time()

        df = next(df_iter)
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print("chunk inserted in", (t_end - t_start), "seconds.")

        if len(df) < 100000:
            break

if __name__ == '__main__':
    print("Running!")
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database for postgres')
    parser.add_argument('--table_name', help='name of the table to write results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)