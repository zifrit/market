#!/bin/bash

set -e

psql --username postgres --dbname postgres <<-EOSQL
    CREATE DATABASE $DB_NAME;
EOSQL