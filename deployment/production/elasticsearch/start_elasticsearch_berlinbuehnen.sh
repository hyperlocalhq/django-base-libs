#!/usr/bin/env bash
export ES_HOME=/usr/local/elasticsearch-5.6.9
cd ${ES_HOME}
./bin/elasticsearch -d \
    -p berlinbuehnen_pid \
    -E cluster.name=berlinbuehnen \
    -E node.name=berlinbuehnen \
    -E network.host=127.0.0.1 \
    -E http.port=9201
