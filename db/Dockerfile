FROM postgres:15

WORKDIR /src

COPY bingo/lib/ lib/

COPY bingo/sql/ sql/

COPY bingo/bingo-pg-install.sh .

RUN chmod +x bingo-pg-install.sh

RUN ./bingo-pg-install.sh -y

RUN mv /src/bingo_install.sql /docker-entrypoint-initdb.d/

EXPOSE 5432