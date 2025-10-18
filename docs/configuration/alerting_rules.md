---
title: Alerting rules
sort_rank: 3
---

* Alerting rules
  * == alert conditions /
    * -- based on -- PromQL
    * if they are met (== PromQL expression's return != 0) -> send notifications -- to an -- external service

* restrictions
  * 's names MUST be [valid label values](https://prometheus.io/docs/concepts/data_model/#metric-names-and-labels)

## Defining alerting rules

* Alerting rules' configuration
  * 👀== [recording rules' configuration](recording_rules.md)👀
  * [syntax](recording_rules.md#rule)

* `groups[*].`
  * `labels`
    * == [] of labels /
      * == `key:value`
        * `value`
          * can be templated
      * if there is some conflict with `rules[*].labels` -> are overwritten 
  * `rules[*].`
    * `for`
      * OPTIONAL
      * == duration BETWEEN [FIRST expression found, forTime] / required -- to -- fire this element
    * `keep_firing_for`
      * OPTIONAL
      * == AFTER the condition is NO longer met,
        * how long the alert continues to fire
    * `annotations`
      * == informational labels 
      * == [] of `key:value`
        * `value`
          * can be templated
      * uses
        * longer additional information
          * _Example:_ alert descriptions or runbook links

## Inspecting alerts | runtime

* 👀if there are pending & firing alerts -> Prometheus stores synthetic time series👀
    ```
    ALERTS{alertname="<alert name>", alertstate="<pending or firing>", <additional alert labels>}
    ```

## Sending alert notifications

* Prometheus's 
  * alerting rules
    * use cases
      * figure what is broken *RIGHT NOW*
    * != FULLY-fledged notification solution
  * [configuration](configuration.md)
    * AUTOMATICALLY discover AVAILABLE Alertmanager instances -- through -- its service discovery integrations
    * / periodically send information 
      * -- about -- alert states
      * -- to an -- Alertmanager instance

* [Prometheus Alertmanager](https://prometheus.io/docs/alerting/alertmanager/)
  * | simple alert definitions,
    * provide
      * summarization,
      * notification rate limiting,
      * silencing & alert dependencies
      * dispatch the notifications
