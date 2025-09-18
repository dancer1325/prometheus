---
title: Federation
sort_rank: 6
---

* Federation
  * allows
    * 👀Prometheus server can scrape ANOTHER Prometheus server's time series👀
  * federation payload
    * == MULTIPLE metric families /
      * SAME name
      * DIFFERENT types

    ```yaml
    http_requests (float64)           = 1500.0
    http_requests (counter histogram) = {buckets: [1,5,10], counts: [100,50,25]}
    http_requests (gauge histogram)   = {buckets: [0,1,2], counts: [200,150,100]}
    ```

* native histograms
  * == experimental feature
  * ⚠️Prometheus server's requirements⚠️
    * run -- via -- CL flag `--enable-feature=native-histograms`
      * -> | scraping,
        * protobuf format

    ```yaml
    http_requests_total (counter) = 1000
    http_requests (native histogram) = {detailed bucket data}
    ```

## Use cases

* scale Prometheus monitoring setups
* Prometheus1 pull metrics -- from -- Prometheus2

### Hierarchical federation

* federation topology
  * == tree /
    * higher-level Prometheus servers collect aggregated time series data -- from -- MULTIPLE subordinated Prometheus servers

* _Example:_ [here](examples/federation)

### Cross-service federation

* == Prometheus server / 
  * monitors specifically 1 service
  * ALSO scrape ANOTHER Prometheus server's specific data
    * Reason: 🧠enable alerting & querying🧠

* _Example:_ [here](examples/federation)

## Configuring federation

* `/federate` endpoint
  * exist | ANY Prometheus server
  * allows
    * retrieving current Prometheus server's selected time series
  * ⚠️requirements⚠️
    * specify >= 1 `match[]` URL parameter / specify an [instant vector selector](querying/basics.md#instant-vector-selectors) 
      * Reason: 🧠select the series / expose🧠
      * if there are >1 `match[]` parameters -> select UNION of ALL matched series

* TODO: 
To federate metrics from one server to another, configure your destination
Prometheus server to scrape from the `/federate` endpoint of a source server,
while also enabling the `honor_labels` scrape option (to not overwrite any
labels exposed by the source server) and passing in the desired `match[]`
parameters
* For example, the following `scrape_configs` federates any series
with the label `job="prometheus"` or a metric name starting with `job:` from
the Prometheus servers at `source-prometheus-{1,2,3}:9090` into the scraping
Prometheus:

