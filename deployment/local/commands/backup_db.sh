#!/usr/bin/env bash
#pg_dump --format=c --compress=9 --file=ruhrbuehnen.backup --no-owner ruhrbuehnen
pg_dump --file=ruhrbuehnen.backup --no-owner ruhrbuehnen