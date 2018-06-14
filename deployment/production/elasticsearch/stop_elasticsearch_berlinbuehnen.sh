#!/usr/bin/env bash
export ES_HOME=/usr/local/elasticsearch-5.6.9
cd ${ES_HOME}
kill `cat berlinbuehnen_pid`
