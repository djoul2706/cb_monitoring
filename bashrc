# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# User specific aliases and functions
alias redis_mon='/app/rl/issos/tools/redis/redis-3.0.5/src/redis-cli -p 5044 monitor'
alias HC='curl localhost/healthcheck'
alias COMPIL='curl localhost/mxamo/resource/compilateur'
alias RUNCOMPIL='curl localhost/mxamo/resource/compilateur/run'
alias SUP='curl localhost/mxamo/resource/supervision'
alias RUNSUP='curl localhost/mxamo/resource/supervision/run'

### ELK version 5.6

export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-oracle.x86_64
export LOGSTASH_HOME=/app/rl/issos/tools/logstash/logstash-5.6.4
export ELASTIC_HOME=/app/rl/issos/tools/elasticsearch/elasticsearch-5.6.4
LOGSTASH_LOGS_DIR=/app/rl/logs/issos/logstash
LOGSTASH_CONF_DIR=/app/rl/issos/etc/logstash_conf/
alias OPF='/tools/exploit/scripts/ISSOS_nb_openfile.sh'

# gestion logstash
function start_logstash {
 if [ "$(hostname)" == "$(cat /etc/hosts | grep -E '^186.*.myrlmaster' | awk '{ print $2 }')" ]
 then
  mv $LOGSTASH_CONF_DIR/*jdbc* $LOGSTASH_CONF_DIR/../mysql_master/
 else
  cp $LOGSTASH_CONF_DIR/../mysql_master/* $LOGSTASH_CONF_DIR/
 fi
 $LOGSTASH_HOME/bin/logstash -f $LOGSTASH_CONF_DIR > $LOGSTASH_LOGS_DIR/logstash.out 2> $LOGSTASH_LOGS_DIR/logstash.err --quiet --config.reload.automatic &
}

function stop_logstash {
  pid=$(ps -ef | grep logstash | grep -v "grep" | awk '{ print $2}')
  if test "$pid" -gt 0
   then
    kill $pid
   else
    echo "elasticsearch not started or pidfile not set"
  fi
}

# gestion elastic
alias start_es='$ELASTIC_HOME/bin/elasticsearch -d -p /app/rl/issos/etc/es.pid'
function stop_es {
  if test -s /app/rl/issos/etc/es.pid
   then
    kill $(cat /app/rl/issos/etc/es.pid)
   else
    echo "elasticsearch not started or pidfile not set"
  fi
}
alias es_logs='tail -f /app/rl/logs/issos/elastic/mxa-elk.log'
alias es_hc='curl localhost/es/'
alias INDEX='curl -s localhost/es/_cat/indices?v -u elastic:changeme'

# gestion redis
REDIS_DIR=/app/rl/issos/tools/redis/redis-3.0.5
REDIS_LOGS_DIR=/app/rl/logs/issos/redis
REDIS_CONF_DIR=/app/rl/issos/etc

alias redis_mon='$REDIS_DIR/src/redis-cli -p 5044 monitor'
function start_redis {
    $REDIS_DIR/src/redis-server $REDIS_CONF_DIR/redis.conf &
    pidof src/redis-server > $REDIS_CONF_DIR/redis.pid
    echo "Demarrage redis effectue, process id = $(cat $REDIS_CONF_DIR/redis.pid), logs dispo dans $REDIS_LOGS_DIR"
}
function stop_redis {
   if test -e $REDIS_CONF_DIR/redis.pid
   then
        kill $(cat $REDIS_CONF_DIR/redis.pid)
                rm $REDIS_CONF_DIR/redis.pid
   else
        echo "Erreur lors de la recuperation du PID"
        exit 1
   fi
}
