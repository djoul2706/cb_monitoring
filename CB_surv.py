# -*- coding: utf-8 -*-
import json
import time
import datetime
import urllib2
import urllib
import numpy as np

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
	'hostname' : node_hostname,
	'mem_used' : node_interestingStats["mem_used"],
	'ops' : node_interestingStats["ops"],
	'ep_bg_fetched' : node_interestingStats["ep_bg_fetched"],
	'cpu_utilization_rate' : node_systemStats["cpu_utilization_rate"],
	'swap_used' : node_systemStats["swap_used"],
	'swap_total' : node_systemStats["swap_total"],
	'mem_total' : node_systemStats["cpu_utilization_rate"],
	'mem_free' : node_systemStats["cpu_utilization_rate"]
	}
	return vals

def parse_bucket_stats(data):
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
	vb_active_num_non_resident =  data["op"]["samples"]["vb_active_num_non_resident"]
	vb_active_resident_items_ratio =  data["op"]["samples"]["vb_active_resident_items_ratio"]
	vb_replica_resident_items_ratio =  data["op"]["samples"]["vb_replica_resident_items_ratio"]
	xdc_ops =  data["op"]["samples"]["xdc_ops"]

	vals_json = {
		'datetime' : str(datetime.datetime.now()),
		'cmd_get' : [max(cmd_get),min(cmd_get),sum(cmd_get)/len(cmd_get)],
		'cmd_set' : [max(cmd_set),min(cmd_set),sum(cmd_set)/len(cmd_set)],
		'couch_docs_fragmentation' : [max(couch_docs_fragmentation),min(couch_docs_fragmentation),sum(couch_docs_fragmentation)/len(couch_docs_fragmentation)],
		'cpu_utilization_rate' : [max(cpu_utilization_rate),min(cpu_utilization_rate),sum(cpu_utilization_rate)/len(cpu_utilization_rate)],
		'curr_connections' : [max(curr_connections),min(curr_connections),sum(curr_connections)/len(curr_connections)],
		'ep_bg_fetched' : [max(ep_bg_fetched),min(ep_bg_fetched),sum(ep_bg_fetched)/len(ep_bg_fetched)],
		'ep_cache_miss_rate' : [max(ep_cache_miss_rate),min(ep_cache_miss_rate),sum(ep_cache_miss_rate)/len(ep_cache_miss_rate)],
		'ep_diskqueue_drain' : [max(ep_diskqueue_drain),min(ep_diskqueue_drain),sum(ep_diskqueue_drain)/len(ep_diskqueue_drain)],
		'ep_diskqueue_fill' : [max(ep_diskqueue_fill),min(ep_diskqueue_fill),sum(ep_diskqueue_fill)/len(ep_diskqueue_fill)],
		'ep_flusher_todo' : [max(ep_flusher_todo),min(ep_flusher_todo),sum(ep_flusher_todo)/len(ep_flusher_todo)],
		'ep_oom_errors' : [max(ep_oom_errors),min(ep_oom_errors),sum(ep_oom_errors)/len(ep_oom_errors)],
		'ep_tmp_oom_errors' : [max(ep_tmp_oom_errors),min(ep_tmp_oom_errors),sum(ep_tmp_oom_errors)/len(ep_tmp_oom_errors)],
		'ep_queue_size' : [max(ep_queue_size),min(ep_queue_size),sum(ep_queue_size)/len(ep_queue_size)],
		'ep_resident_items_rate' : [max(ep_resident_items_rate),min(ep_resident_items_rate),sum(ep_resident_items_rate)/len(ep_resident_items_rate)],
		'mem_actual_free' : [max(mem_actual_free),min(mem_actual_free),sum(mem_actual_free)/len(mem_actual_free)],
		'mem_actual_used' : [max(mem_actual_used),min(mem_actual_used),sum(mem_actual_used)/len(mem_actual_used)],
		'mem_free' : [max(mem_free),min(mem_free),sum(mem_free)/len(mem_free)],
		'mem_total' : [max(mem_total),min(mem_total),sum(mem_total)/len(mem_total)],
		'mem_used' : [max(mem_used),min(mem_used),sum(mem_used)/len(mem_used)],
		'mem_used_sys' : [max(mem_used_sys),min(mem_used_sys),sum(mem_used_sys)/len(mem_used_sys)],
		'ops' : [max(ops),min(ops),sum(ops)/len(ops)],
		'swap_total' : [max(swap_total),min(swap_total),sum(swap_total)/len(swap_total)],
		'timestamp' : [max(timestamp),min(timestamp),sum(timestamp)/len(timestamp)],
		'vb_active_num' : [max(vb_active_num),min(vb_active_num),sum(vb_active_num)/len(vb_active_num)],
		'vb_active_num_non_resident' : [max(vb_active_num_non_resident),min(vb_active_num_non_resident),sum(vb_active_num_non_resident)/len(vb_active_num_non_resident)],
		'vb_active_resident_items_ratio' : [max(vb_active_resident_items_ratio),min(vb_active_resident_items_ratio),sum(vb_active_resident_items_ratio)/len(vb_active_resident_items_ratio)],
		'vb_replica_resident_items_ratio' : [max(vb_replica_resident_items_ratio),min(vb_replica_resident_items_ratio),sum(vb_replica_resident_items_ratio)/len(vb_replica_resident_items_ratio)],
		'xdc_ops' : [max(xdc_ops),min(xdc_ops),sum(xdc_ops)/len(xdc_ops)]
		}

	return vals_json


# recuperation des données pour chacun des noeuds 
f = urllib2.urlopen('http://localhost:8091/pools/nodes')
data = json.load(f)

for node in data["nodes"]:
	node_values = parse_node_stats(node)
	print(node_values)

# recuperation des stats pour le bucket
bucket = 'Listes'
zoom = 'hour'
url = 'http://localhost:8091/pools/default/buckets/' + bucket + '/stats?zoom=' + zoom

f = urllib2.urlopen(url)
data = json.load(f)

print(parse_bucket_stats(data))

