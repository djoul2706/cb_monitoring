#!/bin/bash

while (true)
do
#/opt/couchbase/bin/CB_surv.sh | nc 192.168.61.1 5000
python CB_surv.py | nc 192.168.61.1 5000
sleep 5
done
