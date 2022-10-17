#!/bin/bash
tag=$(date "+%Y%m%d%H%M%S")
image_name=taomercy/stock:v1.0-$tag
docker build -t $image_name .
docker push stock:$tag
docker run -id --name=stock-monitor $image_name

