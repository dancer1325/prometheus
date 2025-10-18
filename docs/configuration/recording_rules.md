---
title: Defining recording rules
nav_title: Recording rules
sort_rank: 2
---

## Configuring rules

* Prometheus' rules
  * syntax
    ```yaml
    groups:
      [ - <rule_group> ]
    ```
  * supported types 
    * [recording rules](#recording-rules)
    * [alerting rules](alerting_rules.md)
  * can be
    * configured
      * == define | .yaml
    * evaluated | regular intervals
  * 👀if you want to 
    * include them | Prometheus -> [Prometheus configuration](configuration.md)'s `rule_files` field👀
    * reload them | runtime -> send `SIGHUP` | Prometheus process👀

* alert rule group
  * == MULTIPLE rules /
    * run SEQUENTIALLY | regular interval
    * 👀SAME evaluation time 👀
      * == | evaluate a rule, ALL rules use the SAME timestamp

## Syntax-checking rules

* `promtool`
  * == Prometheus's CL utility tool
    * ALSO included | download [Prometheus binary](https://prometheus.io/download/)
    * allows
      * checking whether a rule file is syntactically correct / ⚠️WITHOUT starting a Prometheus server⚠️

        ```bash
        promtool check rules /path/to/example.rules.yml
        ```
        * if file is 
          * syntactically valid -> 
            * prints parsed rules' textual representation | standard output 
            * returns `0`
          * NOT syntactically valid OR invalid input arguments ->
            * prints an error message | standard error
            * returns `1`

## Recording rules

* Recording rules
  * 👀organized | rule group👀
  * allow you to
    * 💡about frequently needed OR computationally expensive expressions💡
      * precompute 
        * -> | query, MUST faster
      * save their result -- as a -- 👀NEW set of time series👀
  * uses
    * dashboards
      * Reason: 🧠query the SAME expression REPEATEDLY / EACH refresh🧠
  * restrictions
    * 's names MUST be [valid metric names](https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)

### `<rule_group>`

```yaml
# The name of the group. Must be unique within a file.
name: <string>

# How often rules in the group are evaluated.
[ interval: <duration> | default = global.evaluation_interval ]

# Limit the number of alerts an alerting rule and series a recording
# rule can produce. 0 is no limit.
[ limit: <int> | default = 0 ]

# Offset the rule evaluation timestamp of this particular group by the specified duration into the past.
[ query_offset: <duration> | default = global.rule_query_offset ]

# Labels to add or overwrite before storing the result for its rules.
# Labels defined in <rule> will override the key if it has a collision.
labels:
  [ <labelname>: <labelvalue> ]

rules:
  [ - <rule> ... ]
```

### `<rule>`

* recording rule's syntax

    ```yaml
    # The name of the time series to output to. Must be a valid metric name.
    record: <string>
    
    # == PromQL expression / evaluate. Every evaluation cycle this is
    # evaluated at the current time, and the result recorded as a new set of
    # time series with the metric name as given by 'record'.
    expr: <string>
    
    # BEFORE storing the result, labels / add OR overwrite 
    labels:
      [ <labelname>: <labelvalue> ]
    ```

* alerting rule's syntax 

    ```yaml
    # The name of the alert. Must be a valid label value.
    alert: <string>
    
    # The PromQL expression to evaluate. Every evaluation cycle this is
    # evaluated at the current time, and all resultant time series become
    # pending/firing alerts.
    expr: <string>
    
    # Alerts are considered firing once they have been returned for this long.
    # Alerts which have not yet fired for long enough are considered pending.
    [ for: <duration> | default = 0s ]
    
    # How long an alert will continue firing after the condition that triggered it
    # has cleared.
    [ keep_firing_for: <duration> | default = 0s ]
    
    # Labels to add or overwrite for each alert.
    labels:
      [ <labelname>: <tmpl_string> ]
    
    # Annotations to add to each alert.
    annotations:
      [ <labelname>: <tmpl_string> ]
    ```

* [naming metrics' best practices](https://prometheus.io/docs/practices/rules/#recording-rules)

## Limiting alerts and series

* TODO:
A limit for alerts produced by alerting rules and series produced recording rules can be configured per-group
* When the limit is exceeded, _all_ series produced
by the rule are discarded, and if it's an alerting rule, _all_ alerts for
the rule, active, pending, or inactive, are cleared as well
* The event will be
recorded as an error in the evaluation, and as such no stale markers are
written.

## Rule query offset
This is useful to ensure the underlying metrics have been received and stored in Prometheus
* Metric availability delays are more likely to occur when Prometheus is running as a remote write target due to the nature of distributed systems, but can also occur when there's anomalies with scraping and/or short evaluation intervals.

## Failed rule evaluations due to slow evaluation

If a rule group hasn't finished evaluating before its next evaluation is supposed to start (as defined by the `evaluation_interval`), the next evaluation will be skipped
* Subsequent evaluations of the rule group will continue to be skipped until the initial evaluation either completes or times out
* When this happens, there will be a gap in the metric produced by the recording rule
* The `rule_group_iterations_missed_total` metric will be incremented for each missed iteration of the rule group.
