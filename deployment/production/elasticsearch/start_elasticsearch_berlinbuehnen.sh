#!/usr/bin/env bash
export ES_HOME=/usr/local/elasticsearch-5.6.9
cd ${ES_HOME}
./bin/elasticsearch -d -p berlinbuehnen_pid -Ecluster.name=berlinbuehnen -Enode.name=berlinbuehnen -Enetwork.host=127.0.0.1 -Ehttp.port=9201
