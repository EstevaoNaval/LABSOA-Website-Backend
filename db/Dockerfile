FROM postgres:15

WORKDIR /app

COPY bingo/lib/ lib/

COPY bingo/sql/ sql/

COPY bingo/bingo-pg-install.sh .

RUN chmod +x bingo-pg-install.sh

RUN ./bingo-pg-install.sh -y

RUN mv /app/bingo_install.sql /docker-entrypoint-initdb.d/

EXPOSE 5432