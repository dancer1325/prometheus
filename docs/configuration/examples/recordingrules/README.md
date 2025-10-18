* goal
  * configuring rules
  * syntax-checking rules

# requirements

* install [Prometheus & Promtool](/prometheus/README.md#install) OR install docker

# Prometheus' rules
* `docker compose up -d` / `1.` comment

## evaluated | regular intervals
* | browser, http://localhost:9090
  * query, graph
    ```text
    ## check NUMBER of evaluations /  group
    prometheus_rule_evaluations_total{rule_group="/etc/prometheus/simple_rulefile.yml;frequent-checks"}
    
    ## check LAST evaluation
    prometheus_rule_group_last_evaluation_timestamp_seconds{rule_group="example"}
    ```
    * ⚠️adjust the timing in the graph to visualize it⚠️

## if you want to reload Prometheus rule | runtime -> `SIGHUP` | Prometheus process
* | RANDOM path,
  * `ps aux | grep prometheus`
  * `kill -SIGHUP PREVIOUS_PID_GOT`
* | terminal running prometheus
  * display log message "Completed loading of configuration file ..."

# alert rule group == MULTIPLE rules /
## run SEQUENTIALLY | regular interval
* TODO:
## SAME evaluation time == | evaluate a rule, ALL rules use the SAME timestamp
* TODO:

# syntax-checking rules

## syntactically valid
* steps
  * | this path,
    * `promtool check rules recording_rules_withouterrors.yml`
      * print success 

## syntactically NOT valid
* steps
  * | this path,
    * `promtool check rules recording_rules_witherror.yml`
      * print the error

# recording rules
## precompute == faster
* `docker compose up -d`
* http://localhost:9090/rules
  * check the rules
* TODO: how to check ?
## save their result -- as a -- NEW set of time series
* http://localhost:9090/query
  * `handler:http_latency_ratio:5m`
  * `job:http_request_rate:5m`
## restrictions: 's names valid metric names
* TODO:

# alerting rules

* TODO:
