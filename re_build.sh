#! /bin/sh
cd /home/iguana/iguana
git stash
git pull
git stash pop
docker-compose up -d --build web 

