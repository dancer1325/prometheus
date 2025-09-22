* goal
  * Alertmanager's UI

# Requirements
* [install](/prometheus-alertmanager/README.md#install)
* | root path,
  * `prometheus --config.file=docs/configuration/examples/alertingrules/prometheus.yml`
* wait for 1' / alerts triggered

# `groups[*].labels` can be overwritten with `groups[*].rules[*].labels`
* http://localhost:9090/alerts
* check label is `team: myteamoverwritten`

