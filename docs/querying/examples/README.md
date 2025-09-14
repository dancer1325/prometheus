* goal
    * querying

# requirements

* install [Prometheus & Promtool](/prometheus/README.md#install)
* `make assets`
* `pip install prometheus_client`

# run Prometheus

* | this path,
  * `python3 mock-apiserver.py`
* | root path,
  * `prometheus --config.file=docs/querying/examples/prometheus-apiserver-config.yml --web.listen-address=:9090`
