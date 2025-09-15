---
title: Getting started
sort_rank: 1
---

* goal
  * how to 
    * install,
    * configure /
      * scrape itself & example application 
    * use 1 simple Prometheus instance
    * work with queries + rules + graphs /
      * used | collected time series data

## Downloading
* [here](installation.md)

## Configuring Prometheus to monitor itself

* Prometheus
  * collects targets' metrics
    * -- by -- scraping metrics HTTP endpoints
    * 💡EVEN OWN Prometheus' metrics💡
      * Reason:🧠Prometheus exposes data🧠

## Starting Prometheus

* | start Prometheus,
  * 👀Prometheus create its database👀
    * by default, | "./data/"
    * if you want to specify the location -> CL flag `--storage.tsdb.path`
  * [localhost:9090/metrics](http://localhost:9090/metrics)
    * == 💡metrics / served -- by -- Prometheus💡
      * _Example:_ `prometheus_target_interval_length_seconds`

## Using the graphing interface

* | http://localhost:9090/query & "Graph" tab

## Starting up some sample targets

* goal
  * add ADDITIONAL targets / Prometheus can scrape

* [Node Exporter](https://prometheus.io/docs/guides/node-exporter/)
  * follow [this guide](https://github.com/dancer1325/prometheus-website/blob/main/docs/guides/node-exporter.md)

## Configure Prometheus / monitor the sample targets

* group MULTIPLE endpoints | 1! job
* follow [this](examples/gettingStarted/README.md#configure-prometheus--monitor-the-sample-targets)

## Configure rules for aggregating scraped data | NEW time series

* ⚠️if queries aggregate thousands of time series & you compute -> can get slow ⚠️ 
  * NOT | our example
  * Solution: 💡Prometheus can prerecord expressions | NEW persisted time series -- via -- configured _recording rules_💡
    * 👀== create a NEW metric👀
    * include | Prometheus, -- via -- `rule_files`

## Reloading configuration

* [here](configuration/configuration.md)

## Shutting down your instance gracefully

* Prometheus
  * have recovery mechanisms

* if there is an abrupt process failure -> use signals OR interrupts
  * Reason:🧠clean shutdown of a Prometheus instance🧠
  * ways
    * | Linux,
      * send `SIGTERM` or `SIGINT` signals -- to the -- Prometheus process
        ```bash
        kill -s <SIGNAL> <PrometheusPID>
        ```
