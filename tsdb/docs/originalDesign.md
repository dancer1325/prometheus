https://web.archive.org/web/20210803115658/https://fabxc.org/tsdb/

* goal
  * Writing a Time Series Database from Scratch

* Prometheus
  * == monitoring system /
    * == custom time series database (TSDB) + its well-integration with Kubernetes
      * Reason why well-integrations with Kubernetes: 🧠query language + operational model🧠
  * use cases
    * workloads MORE dynamic
      * _Example:_ ephemeral containers, automatic auto-scaling, distributed microservices, ...
      * cons
        * ⚠️performance problems (MORE memory, MORE storage, ...) -> impacts monitoring system⚠️
      * 👀handled pretty well by Prometheus👀
        * 1! Prometheus’s server can ingest
          * \< 1 million samples / second
          * \>1 million time series / occupy small amount of disk space
  * 's storage
    * CURRENT,
      * SOME inefficiencies
    * PROPOSAL,
      * NEW designed storage subsystem / 
        * corrects inefficiencies
        * handle NEXT order of scale

# CURRENT problems
## Time series data
* TODO:

## Vertical and Horizontal
* TODO:

## TODO: