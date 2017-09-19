#!/bin/bash
COUCHBASE_BINS=/opt/couchbase/bin

vals=`$COUCHBASE_BINS/cbstats localhost:11210 -b Listes all | grep -E "curr_connections|rejected_conns|ep_bg_fetched|ep_queue_size|vb_replica_eject|vb_active_curr_items|mem_used|ep_mem_high_wat|ep_mem_high_wat_percent|vb_active_num|vb_active_perc_mem_resident|cmd_get|cmd_set|ep_tmp_oom_errors|ep_total_cache_size" | sed 's/ //g' | tr '\n' ' ' | sed 's/:/=/g'`


nb_proc_smb=$(ps -ef | grep beam.smp | grep -v "grep" | wc -l)

echo "$(date "+%Y-%m-%d %H:%M:%S") $(hostname) $vals nb_proc_smb=$nb_proc_smb"