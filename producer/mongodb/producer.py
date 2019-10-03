import subprocess
import pymongo
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
    mongo_client = pymongo.MongoClient('mongodb://mongodb:27017')
    break
  except Exception as e:
    print('Received error while connecting to server ', e)
    print('Going to sleep')
    time.sleep(10)

config = {'_id': 'rs0', 'members': [{'_id': 0, 'host': 'mongodb:27017'}]}
mongo_client.admin.command("replSetInitiate", config)

maf_db = mongo_client.maf
person_ids_collection = maf_db.person_ids

with open(unzipped_file_name) as input_file:
    for record in input_file:
        try:
            dict_record = json.loads(record)
            # Sample data:
            # {"adult":false,"id":658,"name":"Alfred Molina","popularity":9.314}
            insert_operation = person_ids_collection.insert_one(dict_record)
            print("Record inserted: ", insert_operation.inserted_id)
            # Sleep for random time to get varying ingestion rate in mysql and hence in kafka
            time.sleep(random())
        except Exception as e:
            print('Could not send record: ', e)
