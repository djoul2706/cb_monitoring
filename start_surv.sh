#!/bin/bash

while (true)
do
/opt/couchbase/bin/CB_surv.sh | nc 172.17.0.1 5000
sleep 5
done