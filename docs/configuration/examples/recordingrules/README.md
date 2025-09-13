* goal
  * configuring rules
  * syntax-checking rules

# requirements

* install [Prometheus & Promtool](/prometheus/README.md#install)
* `make assets`

# configuring rules

* _Example:_ [simple_rulefile.yaml](simple_rulefile.yaml)

* steps
  * | root path,
    * `prometheus --config.file=docs/configuration/examples/recordingrules/prometheus.yml --web.listen-address=:9090`
  * | browser, http://localhost:9090
    * status, rule health
      * check existing rule

* evaluated | regular intervals
  * steps
    * | browser, http://localhost:9090
      * query, graph
        ```text
        ## check NUMBER of evaluations /  group
        prometheus_rule_evaluations_total{rule_group="docs/configuration/examples/recordingrules/simple_rulefile.yaml;example"}
        
        ## check LAST evaluation
        prometheus_rule_group_last_evaluation_timestamp_seconds{rule_group="example"}
        ```
        * ⚠️adjust the timing in the graph to visualize it⚠️

* reload Prometheus rule | runtime
  * steps
    * | RANDOM path,
      * `ps aux | grep prometheus`
      * `kill -SIGHUP PREVIOUS_PID_GOT`
    * | terminal running prometheus
      * display log message "Completed loading of configuration file ..."

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

* TODO:
