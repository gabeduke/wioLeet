#!/bin/bash

TAG=${1}

docker build -t dukeman/wioleet:${TAG} .
docker push dukeman/wioleet:${TAG}