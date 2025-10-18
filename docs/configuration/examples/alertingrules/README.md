* goal
  * Alertmanager's UI

# Requirements
* [install](/prometheus-alertmanager/README.md#install)
* | this path,
  * `docker compose up -d`

# Alerting rules
## == alert conditions /
### -- based on -- PromQL
+ see [simple-alerting.yml](simple-alerting.yml)'s `groups[*].rules[*].expr`

## define
+ see [simple-alerting.yml](simple-alerting.yml)
### `groups[*].labels` can be overwritten -- with -- `groups[*].rules[*].labels`
* http://localhost:9090/alerts > Prometheus-monitoring > PrometheusDown
  * label `alerting: prometheus-down`
### `groups[*].rules[*]`
#### `.for`
##### OPTIONAL
* http://localhost:9090/alerts > prometheus-monitoring > PrometheusTooManyRestarts
#### `.keep_firing_for`
##### OPTIONAL
* http://localhost:9090/alerts > NONE have it


## if there are pending & firing alerts -> Prometheus stores synthetic time series
* http://localhost:9090/query
  * `ALERTS`
