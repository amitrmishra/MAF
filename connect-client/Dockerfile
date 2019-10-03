FROM python

RUN mkdir /connectors
COPY register-mongodb.json /connectors/register-mongodb.json
COPY register-mysql.json /connectors/register-mysql.json
COPY register-postgres.json /connectors/register-postgres.json

COPY create-connectors.py /connectors/create-connectors.py

WORKDIR /connectors

RUN pip install requests

CMD python create-connectors.py register-mongodb.json register-mysql.json register-postgres.json && \
    tail -f /dev/null
