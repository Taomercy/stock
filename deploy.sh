#!/bin/bash
build_tag=`git rev-parse --short HEAD`
docker build -t taomercy/stock-monitor:${build_tag} .
docker push taomercy/stock-monitor:${build_tag}
docker ps -a | grep stock-monitor | awk {'print $1'} | xargs docker stop
docker ps -a | grep stock-monitor | awk {'print $1'} | xargs docker rm
docker run -id --name=stock-monitor taomercy/stock-monitor:${build_tag}
