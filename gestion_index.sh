#!/bin/bash

curl -s -u elastic:changeme 'localhost/es/_cat/indices?v' | grep '[0-9]\{4\}.[0-9]\{2\}.[0-9]\{2\}'  | grep -v tr | sort > /tmp/liste_index
cat /tmp/liste_index | grep open | awk '{ print $3}' > /tmp/liste_index_open
cat /tmp/liste_index | grep close | awk '{ print $2}' > /tmp/liste_index_close

function get_dates {
if [[ "$index" = *"accesslogs"* ]]
then
 date_close=`date -d "5 days ago" "+%s"`
 date_del=`date -d "9 days ago" "+%s"`
else
 date_close=`date -d "5 days ago" "+%s"`
 date_del=`date -d "9 days ago" "+%s"`
fi
}

for index in $(cat /tmp/liste_index_open)
do
    date_index_fichier=`echo $index | grep -o '[0-9]\{4\}.[0-9]\{2\}.[0-9]\{2\}' | sed 's/\./-/g'`
    date_index=`date -d "$date_index_fichier" "+%s"`

    get_dates
    if test "$date_index" -lt "$date_close"
    then
        echo "Index à fermer : $index"
        curl -XPOST -u elastic:changeme "localhost/es/$index/_close"
    fi
    if test "$date_index" -lt "$date_del"
    then
        echo "Index à supprimer : $index"
        curl -XDELETE -u elastic:changeme "localhost/es/$index"
    fi
done

for index in $(cat /tmp/liste_index_close)
do
    date_index_fichier=`echo $index | grep -o '[0-9]\{4\}.[0-9]\{2\}.[0-9]\{2\}' | sed 's/\./-/g'`
    date_index=`date -d "$date_index_fichier" "+%s"`
    get_dates

    if test "$date_index" -lt "$date_close"
    then
        echo "Index à fermer : $index"
        curl -XPOST -u elastic:changeme "localhost/es/$index/_close"
    fi
    if test "$date_index" -lt "$date_del"
    then
        echo "Index à supprimer : $index"
        curl -XDELETE -u elastic:changeme "localhost/es/$index"
    fi
done

rm /tmp/liste_index*
