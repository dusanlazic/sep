#!/bin/sh
docker run -d \
  --name logsea \
  -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  dusanlazic/logsea
