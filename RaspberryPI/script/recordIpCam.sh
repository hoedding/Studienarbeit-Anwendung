# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				           #
# Mail: mail[at]timohoeting.de  			         #
################################################
# Mit FFMPEG wird der Stream eingelesen und mit
# 3 FPS in Bilder gewandelt

name=date +%Y-%m-%d_%H.%M.%S.$((RANDOM%100000))
path=$1
ip=$2
user=$3
pw=$4
image=$path/img/

ffmpeg -i rtsp://$user:$pw@$ip:554 -f image2 -vf fps=3 $image$name%03d.jpg -loglevel quiet
