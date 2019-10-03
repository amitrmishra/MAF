FROM python

LABEL maintainer="Amit Ranjan"

COPY producer.py /producer.py

ENV FILE_PREFIX=movie_ids

RUN pip install mysql-connector;

#CMD tail -f /dev/null
#CMD sleep 10 && python /producer.py

CMD python /producer.py
