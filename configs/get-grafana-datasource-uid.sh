#!/bin/bash
DATASOURCE_NAME="$1"
TIMEOUT=300
START_TIME=$(date +%s)

until curl -s http://localhost:3000/api/health | grep -q '"status":"ok"'; do
  sleep 5
  CURRENT_TIME=$(date +%s)
  if [ $((CURRENT_TIME - START_TIME)) -gt $TIMEOUT ]; then
    echo "Error: Timeout waiting for Grafana to start" >&2
    exit 1
  fi
done

DATASOURCES=$(curl -s -u admin:admin http://localhost:3000/api/datasources)
PROM_UID=$(echo "$DATASOURCES" | jq -r --arg name "$DATASOURCE_NAME" '.[] | select(.name == $name) | .uid')
if [ -z "$PROM_UID" ]; then
  echo "Error: Failed to fetch UID for data source '$DATASOURCE_NAME'" >&2
  exit 1
fi

echo "$PROM_UID"