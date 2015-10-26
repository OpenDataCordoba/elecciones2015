rsync -av --progress --rsh='ssh -p 987' ../api opendata@opendatacordoba.org:/home/opendata/www/elecciones2015/
ssh -p 987 opendata@opendatacordoba.org "find /home/opendata/www/elecciones2015/api -type d -exec chmod 755 {} \;"
ssh -p 987 opendata@opendatacordoba.org "find /home/opendata/www/elecciones2015/api -type f -exec chmod 644 {} \;"

