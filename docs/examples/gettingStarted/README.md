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

# start some node-exporters

* steps
  * | [node_exporter](node_exporter-1.9.1.darwin-arm64)
    * start 3 node exporters / expose metrics | DIFFERENT ports 
      * `./node_exporter --web.listen-address 127.0.0.1:8080`
      * `./node_exporter --web.listen-address 127.0.0.1:8081`
      * `./node_exporter --web.listen-address 127.0.0.1:8082`
    * check the metrics exposed
      * | browser,
        * http://localhost:8080/metrics
        * http://localhost:8081/metrics
        * http://localhost:8082/metrics

# Configure Prometheus / monitor the sample targets

* | [prometheus.yaml](prometheus.yml),
  * add

    ```yaml
      - job_name: node
        static_configs:
          - targets: ['localhost:8080', 'localhost:8081']
            labels:
              group: 'production'
    
          - targets: ['localhost:8082']
            labels:
              group: 'canary'
    ```

* steps
  * | root path,
    * `prometheus --config.file=docs/examples/gettingStarted/prometheus.yml`
  * | browser,
    * http://localhost:9090/query?,
      * `node_cpu_seconds_total`

# Configure rules for aggregating scraped data | NEW time series

* steps
  * | browser,
    * http://localhost:9090/query?,
      * `avg by (job, instance, mode) (rate(node_cpu_seconds_total[5m]))` | graph
  * create [prometheus.rules.yml](prometheus.rules.yml)
  * include the [Prometheus rule](prometheus.rules.yml) | [prometheus](prometheus.yml)
  * run again
    * | root path,
      * `prometheus --config.file=docs/examples/gettingStarted/prometheus.yml`
  * | browser,
    * http://localhost:9090/metrics
      * look up, "cpu-node"
    * http://localhost:9090/query
      * `job_instance_mode:node_cpu_seconds:avg_rate5m`
 
# shut down your instances gracefully
* steps
  * `ps aux | grep prometheus`
    * find your Prometheus PID
  * `kill -s <SIGNAL> <PrometheusPID>`
    * `kill -s SIGTERM <PrometheusPID>`
    * `kill -s SIGINT <PrometheusPID>`

