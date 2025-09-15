* goal
  * getting started

# requirements

* install [Prometheus & Promtool](/prometheus/README.md#install)
* `make assets`

# start Prometheus

* | this path,
  * `prometheus --config.file=prometheus.yml`
    * check how "./data/" is created AUTOMATICALLY
  * `prometheus --config.file=prometheus.yml --storage.tsdb.path=customData`
    * specify the Prometheus' database location

* | browser,
  * http://localhost:9090/metrics
    * == metrics / served -- by -- Prometheus
  * http://localhost:9090/graph
    * ❌NO such file or directory❌
      * Reason:🧠Prometheus UI not set | established🧠
      * Solutions:
        * Solution1: 
          * | root path,
            * `prometheus --config.file=docs/examples/gettingStarted/prometheus.yml`
          * | browser,
            * http://localhost:9090/query & click graph
        * Solution2:
          * | [ui](/prometheus/web/ui),
            * `npm run start`
          * | browser,
            * http://localhost:5173/query & click graph

# first queries
* | browser,
  * http://localhost:9090/query,
    * `prometheus_target_interval_length_seconds`
      * 's return
        * time series / DIFFERENT labels (`quantile`)
    * `prometheus_target_interval_length_seconds{quantile="0.99"}`
      * 's return
        * time series / filter in by 99th percentile latencies
    * `count(prometheus_target_interval_length_seconds)`
      * 's return
        * NUMBER of returned time series

# Using the graphing interface
* | browser,
  * http://localhost:9090/query, "Graph" tab
    * `rate(prometheus_tsdb_head_chunks_created_total[1m])`

# 
