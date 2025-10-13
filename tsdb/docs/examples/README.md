# CURRENT problems
## metric name == ANOTHER label dimension
* `docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus`
* http://localhost:9090/
  * `prometheus_http_requests_total` == `{__name__="prometheus_http_requests_total"}`
