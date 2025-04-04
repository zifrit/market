#!/bin/bash

set -e

psql --username postgres --dbname postgres <<-EOSQL
    CREATE DATABASE $POSTGRES_NAME;
EOSQL