rsync -av --progress --rsh='ssh -p 987' ../api opendata@opendatacordoba.org:/home/opendata/www/elecciones2015/
find ../api -type d -exec chmod 755 {} \;