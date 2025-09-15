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

* TODO: Let's add additional targets for Prometheus to scrape.

The Node Exporter is used as an example target, for more information on using it
[see these instructions.](https://prometheus.io/docs/guides/node-exporter/)

```bash
tar -xzvf node_exporter-*.*.tar.gz
cd node_exporter-*.*

# Start 3 example targets in separate terminals:
./node_exporter --web.listen-address 127.0.0.1:8080
./node_exporter --web.listen-address 127.0.0.1:8081
./node_exporter --web.listen-address 127.0.0.1:8082
```

You should now have example targets listening on http://localhost:8080/metrics,
http://localhost:8081/metrics, and http://localhost:8082/metrics.

## Configure Prometheus to monitor the sample targets

Now we will configure Prometheus to scrape these new targets. Let's group all
three endpoints into one job called `node`. We will imagine that the
first two endpoints are production targets, while the third one represents a
canary instance. To model this in Prometheus, we can add several groups of
endpoints to a single job, adding extra labels to each group of targets. In
this example, we will add the `group="production"` label to the first group of
targets, while adding `group="canary"` to the second.

To achieve this, add the following job definition to the `scrape_configs`
section in your `prometheus.yml` and restart your Prometheus instance:

```yaml
scrape_configs:
  - job_name:       'node'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:8080', 'localhost:8081']
        labels:
          group: 'production'

      - targets: ['localhost:8082']
        labels:
          group: 'canary'
```

Go to the expression browser and verify that Prometheus now has information
about time series that these example endpoints expose, such as `node_cpu_seconds_total`.

## Configure rules for aggregating scraped data into new time series

Though not a problem in our example, queries that aggregate over thousands of
time series can get slow when computed ad-hoc. To make this more efficient,
Prometheus can prerecord expressions into new persisted
time series via configured _recording rules_. Let's say we are interested in
recording the per-second rate of cpu time (`node_cpu_seconds_total`) averaged
over all cpus per instance (but preserving the `job`, `instance` and `mode`
dimensions) as measured over a window of 5 minutes. We could write this as:

```
avg by (job, instance, mode) (rate(node_cpu_seconds_total[5m]))
```

Try graphing this expression.

To record the time series resulting from this expression into a new metric
called `job_instance_mode:node_cpu_seconds:avg_rate5m`, create a file
with the following recording rule and save it as `prometheus.rules.yml`:

```yaml
groups:
- name: cpu-node
  rules:
  - record: job_instance_mode:node_cpu_seconds:avg_rate5m
    expr: avg by (job, instance, mode) (rate(node_cpu_seconds_total[5m]))
```

To make Prometheus pick up this new rule, add a `rule_files` statement in your `prometheus.yml`. The config should now
look like this:

```yaml
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s # Evaluate rules every 15 seconds.

  # Attach these extra labels to all timeseries collected by this Prometheus instance.
  external_labels:
    monitor: 'codelab-monitor'

rule_files:
  - 'prometheus.rules.yml'

scrape_configs:
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

  - job_name:       'node'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:8080', 'localhost:8081']
        labels:
          group: 'production'

      - targets: ['localhost:8082']
        labels:
          group: 'canary'
```

Restart Prometheus with the new configuration and verify that a new time series
with the metric name `job_instance_mode:node_cpu_seconds:avg_rate5m`
is now available by querying it through the expression browser or graphing it.

## Reloading configuration

As mentioned in the [configuration documentation](configuration/configuration.md) a
Prometheus instance can have its configuration reloaded without restarting the
process by using the `SIGHUP` signal. If you're running on Linux this can be
performed by using `kill -s SIGHUP <PID>`, replacing `<PID>` with your Prometheus
process ID.

## Shutting down your instance gracefully.

While Prometheus does have recovery mechanisms in the case that there is an
abrupt process failure it is recommended to use signals or interrupts for a
clean shutdown of a Prometheus instance. On Linux, this can be done by sending
the `SIGTERM` or `SIGINT` signals to the Prometheus process. For example, you
can use `kill -s <SIGNAL> <PID>`, replacing `<SIGNAL>` with the signal name
and `<PID>` with the Prometheus process ID. Alternatively, you can press the
interrupt character at the controlling terminal, which by default is `^C` (Control-C).
