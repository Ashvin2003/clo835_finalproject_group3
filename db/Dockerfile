FROM mysql:8.0

COPY db/mysql.sql /tmp

CMD [ "mysqld", "--init-file=/tmp/mysql.sql" ]