# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  			         #
################################################
# Löscht im Rhytmus von 60 Sekunden alle Dateien
# die älter als 60 Sekunden sind

image=$1'/img/'
while true; do
  find $image -type f -mmin +1 -delete
  sleep 60
done
