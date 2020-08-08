 
# Initial database setup

sudo su - postgres
psql

# Inside postgres commands

CREATE DATABASE monorbit;
CREATE USER mono WITH PASSWORD 'iamtheman';
ALTER ROLE mono SET client_encoding TO 'utf8';
ALTER ROLE mono SET default_transaction_isolation TO 'read committed';
ALTER ROLE mono SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE monorbit TO mono;
\q
exit