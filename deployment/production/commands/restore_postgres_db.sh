#!/usr/bin/env bash

if [[ $# -eq 0 ]] ; then
    echo "Please provide the path to the *.backup file of the ccb PostgreSQL database, e.g.:"
    echo ""
    echo "    ./restore_postgres_db.sh /path/to/ccb.backup"
    echo ""
    exit 1
fi

FILE="$1"
dropdb --username=pgsql ccb
createdb --username=ccb ccb
pg_restore --dbname=ccb --role=ccb --schema=public "$FILE"