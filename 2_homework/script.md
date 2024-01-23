services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: ny_taxi

docker network create green-taxi-network

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/Ashton/github_Repos/DE-NYC-Taxi/2_homework/green_taxi_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=green-taxi-network01 \
  --name green-db \
postgres:13

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=green-taxi-network01 \
  --name green-admin \
dpage/pgadmin4

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

python green_taxi_script.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_data \
  --url="${URL}"

docker build -t green_taxi_ingest:v001 .

docker run -it \
  --network=green-taxi-network01 \
  green_taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=green-db \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_data \
    --url="${URL}"

docker run -it \
  --network=green-taxi-network01 \
  green_taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_data \
    --url="${URL}"