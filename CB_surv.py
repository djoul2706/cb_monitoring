# -*- coding: utf-8 -*-
import json
import time
import datetime
import urllib2
import urllib
#import numpy as np
import base64
import logging
from logging.handlers import RotatingFileHandler

def init_logger(logfile,loglevel=logging.DEBUG,consolelevel=logging.DEBUG):
	logger = logging.getLogger()

	logger.setLevel(loglevel)
	formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

	file_handler = RotatingFileHandler(logfile, 'a', 1000000, 1)
	file_handler.setLevel(loglevel)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(consolelevel)
	stream_handler.setFormatter(formatter)
	logger.addHandler(stream_handler)

	return logger

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def parse_node_stats(node):
	node_status = node["status"]
	node_clusterMembership = node["clusterMembership"]
	node_hostname = node["hostname"]
	node_interestingStats = node["interestingStats"]
	node_systemStats = node["systemStats"]
	vals = {
	'datetime' : str(datetime.datetime.now()),
	'status' : node_status,
	'clusterMembership' : node_clusterMembership,
	'hostname' : node_hostname
	}
	if len(node_interestingStats) > 0 :
		vals_stat = {
		'mem_used' : node_interestingStats["mem_used"],
		'ops' : node_interestingStats["ops"],
		'ep_bg_fetched' : node_interestingStats["ep_bg_fetched"],
		'cpu_utilization_rate' : node_systemStats["cpu_utilization_rate"],
		'swap_used' : node_systemStats["swap_used"],
		'swap_total' : node_systemStats["swap_total"],
		'mem_total' : node_systemStats["cpu_utilization_rate"],
		'mem_free' : node_systemStats["cpu_utilization_rate"]
		}
		vals = merge_two_dicts(vals, vals_stat)

	return vals

def parse_bucket_stats(data, bucket_name):
	cmd_get =  data["op"]["samples"]["cmd_get"]
	cmd_set =  data["op"]["samples"]["cmd_set"]
	couch_docs_fragmentation =  data["op"]["samples"]["couch_docs_fragmentation"]
	cpu_utilization_rate =  data["op"]["samples"]["cpu_utilization_rate"]
	curr_connections =  data["op"]["samples"]["curr_connections"]
	ep_bg_fetched =  data["op"]["samples"]["ep_bg_fetched"]
	ep_cache_miss_rate =  data["op"]["samples"]["ep_cache_miss_rate"]
	ep_diskqueue_drain =  data["op"]["samples"]["ep_diskqueue_drain"]
	ep_diskqueue_fill =  data["op"]["samples"]["ep_diskqueue_fill"]
	ep_flusher_todo =  data["op"]["samples"]["ep_flusher_todo"]
	ep_oom_errors =  data["op"]["samples"]["ep_oom_errors"]
	ep_tmp_oom_errors =  data["op"]["samples"]["ep_tmp_oom_errors"]
	ep_queue_size =  data["op"]["samples"]["ep_queue_size"]
	ep_resident_items_rate =  data["op"]["samples"]["ep_resident_items_rate"]
	mem_actual_free =  data["op"]["samples"]["mem_actual_free"]
	mem_actual_used =  data["op"]["samples"]["mem_actual_used"]
	mem_free =  data["op"]["samples"]["mem_free"]
	mem_total =  data["op"]["samples"]["mem_total"]
	mem_used =  data["op"]["samples"]["mem_used"]
	mem_used_sys =  data["op"]["samples"]["mem_used_sys"]
	ops =  data["op"]["samples"]["ops"]
	swap_total =  data["op"]["samples"]["swap_total"]
	timestamp =  data["op"]["samples"]["timestamp"]
	vb_active_num =  data["op"]["samples"]["vb_active_num"]
	vb_replica_eject =  data["op"]["samples"]["vb_replica_eject"]
	ep_mem_high_wat =  data["op"]["samples"]["ep_mem_high_wat"]
	vb_active_num_non_resident =  data["op"]["samples"]["vb_active_num_non_resident"]
	vb_active_resident_items_ratio =  data["op"]["samples"]["vb_active_resident_items_ratio"]
	vb_replica_resident_items_ratio =  data["op"]["samples"]["vb_replica_resident_items_ratio"]
	xdc_ops =  data["op"]["samples"]["xdc_ops"]

	vals_json = {
		"bucket_name" : bucket_name,
		#"datetime" : str(datetime.datetime.now()),
		"cmd_get" : max(cmd_get),
		"cmd_set" : max(cmd_set),
		"couch_docs_fragmentation" : max(couch_docs_fragmentation),
		"cpu_utilization_rate" : max(cpu_utilization_rate),
		"curr_connections" : max(curr_connections),
		"ep_bg_fetched" : max(ep_bg_fetched),
		"ep_cache_miss_rate" : max(ep_cache_miss_rate),
		"ep_diskqueue_drain" : max(ep_diskqueue_drain),
		"ep_diskqueue_fill" : max(ep_diskqueue_fill),
		"ep_flusher_todo" : max(ep_flusher_todo),
		"ep_oom_errors" : max(ep_oom_errors),
		"ep_tmp_oom_errors" : max(ep_tmp_oom_errors),
		"ep_queue_size" : max(ep_queue_size),
		"ep_resident_items_rate" : max(ep_resident_items_rate),
		"mem_actual_free" : max(mem_actual_free),
		"mem_actual_used" : max(mem_actual_used),
		"mem_free" : max(mem_free),
		"mem_total" : max(mem_total),
		"mem_used" : max(mem_used),
		"mem_used_sys" : max(mem_used_sys),
		"ops" : max(ops),
		"swap_total" : max(swap_total),
		"epoch" : max(timestamp),
		"vb_active_num" : max(vb_active_num),
		"ep_mem_high_wat" : max(ep_mem_high_wat),
		"vb_replica_eject" : max(vb_replica_eject),
		"vb_active_num_non_resident" : max(vb_active_num_non_resident),
		"vb_active_resident_items_ratio" : max(vb_active_resident_items_ratio),
		"vb_replica_resident_items_ratio" : max(vb_replica_resident_items_ratio),
		"xdc_ops" : max(xdc_ops)
		}

	return vals_json

logger = init_logger('activity.log',logging.INFO,logging.WARNING)

while 1:

	# recuperation des données pour chacun des noeuds 
	username = "Administrator"
	password = "password"
	request = urllib2.Request("http://localhost:8091/pools/nodes")
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	
	f = urllib2.urlopen(request)
	data = json.load(f)

	balanced = data["balanced"]
	clusterName = data["clusterName"]
	
	if balanced == false :
		logger.warning("cluster %s is not balanced" % clusterName)
	
	for node in data["nodes"]:
		node_values = parse_node_stats(node)
		logger.info(json.dumps(node_values))

	# recuperation des stats pour le bucket
	bucket = 'travel-sample'
	zoom = 'minute'
	url = 'http://localhost:8091/pools/default/buckets/' + bucket + '/stats?zoom=' + zoom

	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	
	f = urllib2.urlopen(request)
	data = json.load(f)
	
	bucket_values = parse_bucket_stats(data, bucket)
	logger.info(json.dumps(bucket_values))

	time.sleep(15)
