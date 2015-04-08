# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  			         #
################################################
# Bindet ein FTP-Laufwerk mit verschlüsselter Verbindung
# in das Home-Verzeichnis des aktuellen Benutzers ein.

path=$1
ip=$2
user=$3
pw=$4
currentuser=$5

curlftpfs $user:$pw@$ip/$path /home/$currentuser/ftp -o allow_other,disable_eprt,tlsv1,nonempty
