#!/usr/bin/env python3
from prometheus_client import Counter, start_http_server
import time
import random

http_requests_total = Counter('http_requests_total', 'Total HTTP requests', ['handler', 'method'])

def simulate_requests():
    while True:
        # GET requests
        http_requests_total.labels(handler='/api/comments', method='GET').inc()
        http_requests_total.labels(handler='/api/users', method='GET').inc()
        
        # POST requests
        http_requests_total.labels(handler='/api/comments', method='POST').inc()
        http_requests_total.labels(handler='/api/users', method='POST').inc()
        
        time.sleep(2)

if __name__ == '__main__':
    start_http_server(8080)
    simulate_requests()