FROM mongo:3.6

LABEL maintainer="Debezium Community"

#COPY init-inventory.sh /usr/local/bin/
#RUN chmod +x /usr/local/bin/init-inventory.sh

#RUN mongod --fork --logpath /var/log/mongod.log --dbpath /data/db
#RUN sh /usr/local/bin/init-inventory.sh
#RUN mongod --shutdown

#CMD ["mongod", "--replSet", "rs0", "--auth"]

CMD ["mongod", "--replSet", "rs0"]
