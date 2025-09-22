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
## precompute
* steps
  * | root path,
    * `prometheus --config.file=docs/configuration/examples/recordingrules/prometheus-recordingrule.yml --web.listen-address=:9090`
      * Problems:
        * Problem1: NOT found alert rules
          * Attempt1: `- "docs/configuration/examples/recordingrules/test-recording-rules.yml"`
          * Attempt2: 
            * | this path,
              * `prometheus --config.file=prometheus-recordingrule.yml --web.listen-address=:9090`
            * | [ui](/prometheus/web/ui)
              * `npm run start` 
          * Note: SOMETHING MUST be wrongly defined | recording rule
            * Reason: 🧠if you pass "simple_rulefile.yaml" is displayed 🧠
            * `promtool check rules test-recording-rules.yaml` SUCCESS
          * Solution: I was checking in alerts, not in rules -- http://localhost:9090/rules -- 
  * | this path,
    * `./test-performance.sh`
      * Problems:
        * Problem1: "data.result" is empty
          * Solution: use Prometheus' metrics, NOT NodeExporter's metrics
        * Problem2: "... jq '.data.result[0].metric'" returns null
          * Solution: `kill -SIGHUP PREVIOUS_PID_GOT`
        * Problem3: ALMOST SAME timing results
          * Solution: switch to MOST complex queries

## restrictions
* TODO:

# alerting rules

* TODO:
