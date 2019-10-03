# System Design
![Image](images/MAFDataPipeline.jpg)

# Design Description
- Different systems/applications/users push data to the relation/non-relational store
- Using Kafka Connect, we read the binlogs/oplogs of the sources and push changes in real time to Kafka Cluster
- We use KSQL to make any real time transformations, filtering and formatting of the data in Kafka. The data is moved from raw Kafka topic to cleansed Kafka topic
- Using Phoenix kafka consumer, we pull data to Operational Data Store. the Operational Data Store is HBase in our design to enable fast and random access to real time data
- HBase acts as a real time and unified replica of the diverse data sources. It acts as source of data for <b>Real Time Data Analytics</b> or <b>Batch DWH Analytics</b>
- The real time metrics are collected in Prometheus using custom jmx exporters. Metrics are collected from Kafka Connect, Kafka Brokers, KSQL and ODS
- Metrics are exposed in grafana. Alerts are configured directly in Grafana.
- The logs are stored in the central ELK using logstash plugin

# What has been covered in the solution

# Running the solution
cd <PROJECT_DIR>

### Build custom images

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

