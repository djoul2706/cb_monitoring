
# cb_monitoring
script python requetant l'api couchbase 9081 permettant de relever les indicateurs de bon fonctionnement et les principales stats pour 
- l'ensemble des nodes du cluster
- le ou les buckets

Le script relève les 60 dernières valeurs collectées par couchbase et conserve le max relevé (paramétre : zoom = 'minute').

les infos sont stockées dans un fichier activity.log selon le format suivant:

'2018-03-16 17:12:48,685 :: INFO :: {"cmd_set": 0, "mem_used": 227842064, "mem_total": 19870003200, "ep_oom_errors": 0, "curr_connections": 275, "swap_total": 0, "mem_actual_used": 6615687168, "cpu_utilization_rate": 38.30954994511526, "epoch": 1521216767421, "ep_diskqueue_drain": 0, "ep_mem_high_wat": 445644800, "mem_used_sys": 11722256384, "ops": 900.0999000999001, "cmd_get": 0, "ep_diskqueue_fill": 0, "vb_active_resident_items_ratio": 100, "bucket_name": "travel-sample", "vb_active_num_non_resident": 0, "couch_docs_fragmentation": 0, "ep_queue_size": 0, "xdc_ops": 900.0999000999001, "vb_replica_resident_items_ratio": 100, "ep_flusher_todo": 0, "mem_free": 13810286592, "ep_tmp_oom_errors": 0, "ep_cache_miss_rate": 0, "mem_actual_free": 13810286592, "vb_replica_eject": 0, "vb_active_num": 1024, "ep_bg_fetched": 0, "ep_resident_items_rate": 100}
2018-03-16 17:13:48,769 :: INFO :: {"status": "healthy", "swap_used": 0, "clusterMembership": "active", "ops": 0, "swap_total": 0, "hostname": "172.20.0.15:8091", "cpu_utilization_rate": 5.897435897435898, "datetime": "2018-03-16 17:13:48.768904", "mem_used": 48115584, "mem_total": 5.897435897435898, "ep_bg_fetched": 0, "mem_free": 5.897435897435898}
2018-03-16 17:13:48,769 :: INFO :: {"status": "healthy", "swap_used": 0, "clusterMembership": "active", "ops": 0, "swap_total": 0, "hostname": "172.20.0.17:8091", "cpu_utilization_rate": 8.808933002481389, "datetime": "2018-03-16 17:13:48.769713", "mem_used": 48355344, "mem_total": 8.808933002481389, "ep_bg_fetched": 0, "mem_free": 8.808933002481389}
2018-03-16 17:13:48,770 :: INFO :: {"status": "healthy", "swap_used": 0, "clusterMembership": "active", "ops": 0, "swap_total": 0, "hostname": "172.20.0.36:8091", "cpu_utilization_rate": 4.714640198511166, "datetime": "2018-03-16 17:13:48.770255", "mem_used": 47962752, "mem_total": 4.714640198511166, "ep_bg_fetched": 0, "mem_free": 4.714640198511166}
2018-03-16 17:13:48,770 :: INFO :: {"status": "healthy", "swap_used": 0, "clusterMembership": "active", "ops": 0, "swap_total": 0, "hostname": "172.20.0.42:8091", "cpu_utilization_rate": 7.826086956521739, "datetime": "2018-03-16 17:13:48.770774", "mem_used": 48349440, "mem_total": 7.826086956521739, "ep_bg_fetched": 0, "mem_free": 7.826086956521739}
2018-03-16 17:13:48,771 :: INFO :: {"status": "healthy", "swap_used": 0, "clusterMembership": "active", "ops": 0, "swap_total": 0, "hostname": "172.20.0.44:8091", "cpu_utilization_rate": 5.73170731707317, "datetime": "2018-03-16 17:13:48.771302", "mem_used": 35050208, "mem_total": 5.73170731707317, "ep_bg_fetched": 0, "mem_free": 5.73170731707317}'

le user/password est en clair dans le fichier

# execution
python CB_surv.py &

# evolutions 
anonymisation du password
entrée du fichier cible pour le log en paramètre
