# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  			         #
################################################
# Verschiebt alle Dateien, die jünger als 10 Sekunden
# sind in einen anderen Ordner. Dieser Ordner kann
# aus der App aufgerufen werden.
# Wird aufgerufen, wenn die Bewegungssensoren anschlagen.

safe=$1/safe/
image=$1/img/

find $image -type f -newermt '-10 seconds' -exec mv {} $safe \;
