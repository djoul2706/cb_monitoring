#!/bin/bash
db_passwor

if test "$1" == "" ; then echo "merci de passer au moins 1 silo en parametre au format BPR3 BPR4..." ; exit 1 ; fi
if test -e liste_route_service ; then rm liste_route_service ; fi
for silo in "$@"
do
req="select c.route from carto_pce c join supervision_pce s on s.pce_id = c.id  where s.pce_state = 'SERVICE' and c.pilote = 0 and c.silo = '$silo'; "

/tools/MySQL/products/5.6/bin/mysql -h myrlmasterp -P 3306 -u umxamo bmxamo -pPrsDPzbc04_ -Ne "$req" >> liste_route_service 2> /dev/null
done

TS=$(date +%Y%m%d_%H%M)
curl -s plrlap10-app:9088/fetchhr | sed 's/||/ /g' | grep -E "^[1-9]" > fetchhr_$TS

# suppression des routes non utilisees depuis plus de X heures
h_delta=$(( 3600 * 2 ))
h_min=$(( $(date +%s) - $h_delta ))
cat fetchhr_$TS | awk -v h_min=$h_min '{ if ($5/1000 > h_min) print $0 }' > fetchhr_$TS.new
mv fetchhr_$TS.new fetchhr_$TS

rm reequilibrage.sql 2> /dev/null

#################
function continue_anyway {
while true; do
    read -p "Etes vous sur de vouloir continuer ? [oui/non]" yn
    case $yn in
        [oui]* ) break;;
        [non]* ) exit;;
        * ) echo "Merci de repondre oui ou non.";;
    esac
done
return 0
}

get_listes () {

nb_route=$(cat liste_route_service | wc -l)
tot_atm=$(eval cat fetchhr_$TS | grep -E \"$(cat liste_route_service | tr '\n' '|')\" | wc -l)
nb_optim=$(( $tot_atm / $nb_route ))
seuil_haut=$(( $nb_optim + $(( $nb_optim / 5)) ))
seuil_bas=$seuil_haut

if [ ! -s liste_route_service ] ; then return 6 ; fi

echo "Liste des routes a depeupler :"
echo "route nb_atm_avant cible delta"
for route in $(cat liste_route_service)
do
  nb_avant=$(grep -c $route fetchhr_$TS)
  if test $nb_avant -gt $seuil_haut ; then
    nb_atm_a_derouter=$(( $nb_avant - $nb_optim ))
    echo "$route $nb_avant $nb_optim -$nb_atm_a_derouter"
    grep $route fetchhr_$TS | awk '{ print $2 }' | sort -R | head -$nb_atm_a_derouter >> "liste_atms_a_derouter"
    cat "liste_atms_a_derouter" | sort -u > liste_atms_a_derouter.new
    mv liste_atms_a_derouter.new liste_atms_a_derouter
  fi
done

if [ ! -s liste_atms_a_derouter ] ; then return 5 ; fi

echo ""
echo "Liste des routes a peupler : "
echo "route nb_atm_avant cible delta"
for route in $(cat liste_route_service)
do
 nb_avant=$(grep -c $route fetchhr_$TS)
 if test $nb_avant -lt $seuil_bas ; then
  nb_place_dispo=$(( $nb_optim - $nb_avant ))
  echo "$route $nb_avant $nb_optim +$nb_place_dispo"
  echo "$route $nb_place_dispo" >> "liste_route_a_peupler"
 fi
done

}

##################

get_date_sql () {
 date_format="^[0-9]{4}-[0-9]{2}-[0-9]{2}[[:space:]][0-9]{2}:[0-9]{2}:[0-9]{2}$"

 while ( [[ ! "$start_time" =~ $date_format ]] )
 do
  read -p "Entrer une date pour l activation des regles de reequilibrage ? [YYYY-MM-DD HH:MM:SS] : " start_time
  if [[ ! "$start_time" =~ $date_format ]] ; then echo "" ; echo  "Format incorrect" ; echo "" ; fi
 done

 echo "La date de fin est fixee automatiquement 1h apres la date de debut"

}

create_sql () {
        liste_routes=liste_route_a_peupler
        liste_atms=liste_atms_a_derouter
        get_date_sql ## invite de commande pour fixer la date de debut d effet de la regle d affinite
        while read line
        do
                if test $(cat $liste_atms | wc -l) -eq 0 ; then break ; fi
                route=$(echo $line | awk '{ print $1}' )
                nb_atm=$(echo $line | awk '{ print $2}' )
                if [ $nb_atm -ge 0 ] ; then
                # recuperation id route
                echo "SET @id_pce = (select id from carto_pce where route = '$route');" >> reequilibrage.sql
                # creation de la ligne dans binding_rules
                name=Reeq_"$route"_"$(date +%Y%m%d_%H%M)"
                echo "insert into binding_rules (name, brief, active, matricule, event_time, start_time, end_time) values ('$name','Reequilibrage_auto',0,'sc_reequilibrage',0,'$start_time','$start_time' + interval 1 hour) ; " >> reequilibrage.sql
                echo "SET @id_regle = (select max(id) from binding_rules);" >> reequilibrage.sql
                fi
                # alimentation binding_nodes avec les $nb_atm wsid
                while [ $nb_atm -ge 0 ]
                do
                        if test $(cat $liste_atms | wc -l) -eq 0 ; then break ; fi
                        wsid=$(head -1 $liste_atms)
                        if test ${#wsid} -eq 13
                        then
                        echo "insert into binding_nodes values(@id_regle, @id_pce, '$wsid') ;" >> reequilibrage.sql
                        fi
                        (( nb_atm-- ));
                        echo "$(tail -n +2 $liste_atms)" > $liste_atms
                done
        done < $liste_routes
}

######################

function load_sql_file () {
file=$1
    read -p "Creation des regles en base (les regles seront inactives) ? [oui/non]" yn
    case $yn in
        [oui]* ) /tools/MySQL/products/5.6/bin/mysql -h myrlmasterp -P 3306 -u umxamo bmxamo -p < reequilibrage.sql ;;
        [non]* ) exit;;
        * ) echo "Merci de repondre oui ou non.";;
    esac
}

###### MAIN ######

echo ""
read -p "Voulez vous fitrer les atms d une (ou plusieurs) entite donnee ? [30002|30002 30056] : " entites
for entite in $entites
do
   echo "$(cat fetchhr_$TS | grep -c $entite) atms a retirer pour l entite $entite"
   cat fetchhr_$TS | grep -Ev $entite > fetchhr_$TS.tmp
   mv fetchhr_$TS.tmp fetchhr_$TS
done
echo ""

continue_anyway

echo ""
echo "PREPARATION des listes (routes a peupler, atms a deplacer)"
echo ""

get_listes
result=$?

if test "$result" -eq 5 ; then echo "Pas de reequilibrage necessaire " ; rm liste_* fetchhr_$TS ; exit 0
elif test "$result" -eq 6 ; then echo "Pas de route dispo " ; rm liste_* fetchhr_$TS ; exit 0
elif  test "$result" -lt 1
then
 echo ""
 echo "****************************"
 echo ""
 echo "PREPARATION du fichier SQL a inserer dans la base pour creation des regles de bascules"
 echo ""
 create_sql
 echo ""
 echo "Reequilibrage a faire : bascule de $(cat reequilibrage.sql | grep -c "binding_nodes" ) atms"
fi

rm liste_*
rm fetchhr_$TS

echo ""
echo "****************************"
echo ""
echo "CHARGEMENT du fichier SQL pour creation des regles"
echo ""

if test -s reequilibrage.sql ; then load_sql_file ; fi
if test "$?" -eq 0 ; then echo "Fichier charge en base - Les regles sont a verifier puis activer via l IHM MXA" ; echo ""
else echo "Erreur lors du chargement" ; echo ""
fi
