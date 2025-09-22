#!/bin/bash

echo "=== compare performance ==="
echo

# URL de Prometheus
PROM_URL="http://localhost:9090"

echo "1. Complex query (WITHOUT recording rule):"
echo "Expression: Complex aggregation with multiple functions"
echo

time curl -s "${PROM_URL}/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le, handler)) / avg(rate(prometheus_http_requests_total[5m])) by (handler)' \
  | jq '.data.result | length' > /dev/null

echo
echo "2. Simple query (WITH recording rule):"
echo "Expression: handler:http_latency_ratio:5m"
echo

time curl -s "${PROM_URL}/api/v1/query" \
  --data-urlencode 'query=handler:http_latency_ratio:5m' \
  | jq '.data.result | length' > /dev/null

echo
echo "3. Check if the recording rule exists:"
curl -s "${PROM_URL}/api/v1/query" \
  --data-urlencode 'query=handler:http_latency_ratio:5m' \
  | jq '.data.result[0].metric'
