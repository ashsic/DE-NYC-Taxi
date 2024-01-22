services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
      POSTGRES_DB: ny_taxi



docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/Ashton/github_Repos/DE-NYC-Taxi/2_homework/green_taxi_data:/var/lib/postgresql/data \
  -p 5432:5432 \
postgres:13

