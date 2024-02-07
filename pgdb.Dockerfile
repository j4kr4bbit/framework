FROM postgres:15

RUN mkdir -p "$PGDATA" && chmod 700 "$PGDATA"
RUN echo "en_US UTF-8" >> /etc/locale.gen && locale-gen


# RUN apt install -y git build-essential postgresql-server-dev-15

# RUN cd /tmp &&\
# git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git &&\
# cd pgvector &&\
# make && make install

ADD ./init.sql /docker-entrypoint-initdb.d

EXPOSE 5432