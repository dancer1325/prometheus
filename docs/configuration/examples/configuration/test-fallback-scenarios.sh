#!/bin/bash
echo "🧪 Testing fallback scenarios"
echo

echo "📋 Scenario 1: Blank response"
curl -s -H "Accept: application/openmetrics-text;version=1.0.0;q=0.5,text/plain;version=0.0.4;q=0.4" \
  http://localhost:9999/metrics | wc -c
echo

echo "📋 Scenario 2: Unparsable content"
curl -s -H "Accept: application/openmetrics-text;version=1.0.0;q=0.5,text/plain;version=0.0.4;q=0.4" \
  http://localhost:9999/metrics | head -2
echo

echo "📋 Scenario 3: Invalid Content-Type"
curl -s -I -H "Accept: application/openmetrics-text;version=1.0.0;q=0.5,text/plain;version=0.0.4;q=0.4" \
  http://localhost:9999/metrics | grep -i content-type
echo

echo "📋 Scenario 4: Valid response (fallback)"
curl -s -H "Accept: application/openmetrics-text;version=1.0.0;q=0.5,text/plain;version=0.0.4;q=0.4" \
  http://localhost:9999/metrics
echo

echo "💡 Run multiple times to see different random scenarios"