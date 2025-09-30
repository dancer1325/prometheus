---
title: API stability guarantees
nav_title: API stability
sort_rank: 11
---

* Prometheus major version,
  * API stability
  * NO breaking changes for key features

* | 3.x,
  * things stable
    * query language & data model
    * alerting and recording rules
    * ingestion exposition format
    * v1 HTTP API (used by dashboards and UIs), excluding endpoints explicitly marked as experimental
    * Configuration file format (minus the service discovery remote read/write, see below)
    * Rule/alert file format
    * [Remote write sending / 1.0 specification](https://prometheus.io/docs/concepts/remote_write_spec/)
    * Agent mode
    * OTLP receiver endpoint
  * things unstable
    * Any feature listed as experimental or subject to change, including:
      * The [`double_exponential_smoothing` PromQL function](https://github.com/prometheus/prometheus/issues/2458)
      * Remote read and the remote read endpoint
    * Server-side HTTPS & basic authentication
    * Service discovery integrations
      * EXCEPTION: `static_configs`, `file_sd_configs` & `http_sd_config`
    * Go APIs of packages that are part of the server
    * HTML generated -- by the -- web UI
    * The metrics in the /metrics endpoint of Prometheus itself
    * Exact on-disk format. Potential changes however, will be forward compatible and transparently handled by Prometheus
    * The format of the logs
* | 2.x
  * [here](https://prometheus.io/docs/prometheus/2.55/stability/)
