import subprocess
import mysql.connector
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
    mysql_connection = mysql.connector.connect(host="mysql", user="root", passwd="debezium")
    break
  except Exception as e:
    print('Received error while connecting to server ', e)
    print('Going to sleep')
    time.sleep(10)

CREATE_DB_SQL = 'CREATE DATABASE IF NOT EXISTS maf'
CREATE_TBL_SQL = 'CREATE TABLE IF NOT EXISTS maf.movie_ids(adult boolean, id int, original_title varchar(255), popularity float, video boolean)'
INSERT_SQL = 'INSERT INTO maf.movie_ids (adult, id, original_title, popularity, video) VALUES (%s, %d, \'%s\', %f, %s)'

mysql_cursor = mysql_connection.cursor()
mysql_cursor.execute(CREATE_DB_SQL)
mysql_cursor.execute(CREATE_TBL_SQL)
mysql_connection.commit()

with open(unzipped_file_name) as input_file:
    for record in input_file:
      try:
        dict_record = json.loads(record)
        mysql_cursor.execute(INSERT_SQL % (dict_record.get('adult', False), dict_record.get('id', -1), dict_record.get('original_title', 'NULL').replace('\'', '\'\''), dict_record.get('popularity', -1), dict_record.get('video', False)))
        mysql_connection.commit()
        print(mysql_cursor.rowcount, "record inserted.")
        # Sleep for random time to get varying ingestion rate in mysql and hence in kafka
        time.sleep(random())
      except Exception as e:
        print('Could not send record: ', e)


mysql_cursor.close()
mysql_connection.close()
