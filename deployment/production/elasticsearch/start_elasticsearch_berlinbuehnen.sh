#!/usr/bin/env bash
export ES_HOME=/usr/local/elasticsearch-5.6.9
cd ${ES_HOME}
./bin/elasticsearch -d -p ruhrbuehnen_pid -Ecluster.name=ruhrbuehnen -Enode.name=ruhrbuehnen -Enetwork.host=127.0.0.1 -Ehttp.port=9201
