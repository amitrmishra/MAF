cd <PROJECT_DIR>

# Build custom images
cd connect-client
docker build -t connect-client .

cd ../mongodb
docker build -t mongodb .

cd ../producer/mongodb
docker build -t mongodb-producer .

cd ../mysql
docker build -t mysql-producer .

cd ../postgres
docker build -t postgres-producer .

cd ../..

# To launch docker containers
export VERSION=0.9
docker-compose -f docker-compose.yaml up

# To stop the docker containers
docker-compose -f docker-compose.yaml down


# View kafka messages
docker exec -it maf_kafka_1 bash

/kafka/bin/kafka-topics.sh \
  --bootstrap-server kafka:9092 \
  --list

/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server kafka:9092 \
  --property print.key=true \
  --topic mysql.maf.movie_ids

/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server kafka:9092 \
  --property print.key=true \
  --topic postgres.maf.tv_series_ids

/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server kafka:9092 \
  --property print.key=true \
  --topic mongodb.maf.person_ids

