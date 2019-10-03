import subprocess
import psycopg2
from datetime import datetime, timedelta
import sys
import json
from random import random
import time
import os


file_prefix = os.environ.get('FILE_PREFIX')
yesterday_date = (datetime.today() - timedelta(days=1)).strftime('%m_%d_%Y')
unzipped_file_name='{file_prefix}_{yesterday_date}.json'.format(file_prefix=file_prefix, yesterday_date=yesterday_date)
zipped_file_name='{unzipped_file_name}.gz'.format(unzipped_file_name=unzipped_file_name)

subprocess.getstatusoutput('wget http://files.tmdb.org/p/exports/{zipped_file_name}'.format(zipped_file_name=zipped_file_name))
subprocess.getstatusoutput('gunzip {zipped_file_name}'.format(zipped_file_name=zipped_file_name))

for attempt in range(0, 10):
  try:
    postgres_connection = psycopg2.connect(host="postgres", user="postgres", password="postgres", port=5432)
    break
  except Exception as e:
    print('Received error while connecting to server ', e)
    print('Going to sleep')
    time.sleep(10)

postgres_connection.autocommit = True

CREATE_SCHEMA_SQL = 'CREATE SCHEMA maf'
CREATE_TBL_SQL = 'CREATE TABLE maf.tv_series_ids(id integer, original_name varchar(255), popularity real)'
INSERT_SQL = 'INSERT INTO maf.tv_series_ids (id, original_name, popularity) VALUES (%d, \'%s\', %f)'

postgres_cursor = postgres_connection.cursor()
postgres_cursor.execute(CREATE_SCHEMA_SQL)
postgres_cursor.execute(CREATE_TBL_SQL)
postgres_connection.commit()

with open(unzipped_file_name) as input_file:
    for record in input_file:
        try:
            dict_record = json.loads(record)
            postgres_cursor.execute(INSERT_SQL % (dict_record.get('id', -1), dict_record.get('original_name', 'NULL').replace('\'', '\'\''), dict_record.get('popularity', -1)))
            postgres_connection.commit()
            print("Record inserted.")
            # Sleep for random time to get varying ingestion rate in mysql and hence in kafka
            time.sleep(random())
        except Exception as e:
            print('Could not send record: ', e)


postgres_cursor.close()
postgres_connection.close()
