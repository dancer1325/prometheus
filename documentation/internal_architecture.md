# Internal architecture

* Prometheus server
  * == MULTIPLE internal components / work together
  * ' architecture

    ![Prometheus server architecture](images/internal_architecture.svg)
    * arrows
      * == request OR connection initiation direction
        * != dataflow direction

## Main function

* [`main()` function](/prometheus/cmd/prometheus/main.go)
  * ' goal
    * initializes & runs ALL OTHER Prometheus server components
    * connects interdependent components -- to -- EACH OTHER
  * steps
    * server's CL flags are defined & parsed -- into a -- [local configuration structure (`flagConfig`)](/prometheus/cmd/prometheus/main.go)
      * != configuration / later read -- from a -- configuration file
        * _Example:_ provided -- by the -- `--config.file` flag 
    * sanitize & initialize SOME values
    * instantiates ALL major Prometheus' run-time components
    * connect Prometheus' run-time components -- via -- 
      * channels + references, OR
      * contexts
    * Prometheus server runs ALL components -- as an -- [actor-like model](https://www.brianstorti.com/the-actor-model/) 
      * == EACH Prometheus' component == INDEPENDENT actor /
        * 's logic is executed / OWN goroutine
        * communicate to -- , via channels, -- OTHER ' components
      * / 
        * [`oklog/pkg/group`](https://pkg.go.dev/github.com/oklog/run) coordinates ALL interconnected actors
          * responsible for
            * startup
            * shutdown
          * execute ALL components parallel
        * if you want to configure the components initialization order -> define MULTIPLE channels
          * _Example of order:_
            * storage
            * load configuration
            * UI

* Prometheus' run-time components ==
  * service discovery, 
  * target scraping, 
  * storage,
  * ...

## Configuration

* types of configurations
  * flag-based configuration
    * == `--config.file`
    * uses
      * simple settings
      * configure immutable system parameters
        * _Examples:_ storage locations, amount of data / keep | disk & memory, 
    * cons
      * if you want to update -> you need to restart the server
  * file-based configuration
    * == ".yaml"
    * pros
      * support hot reload
    * uses
      * scraping [jobs + jobs' instances](https://prometheus.io/docs/concepts/jobs_instances/)
      * [rule files -- to -- load](/prometheus/docs/configuration/recording_rules.md#configuring-rules)

* Prometheus server
  * responsible, about the configuration, for
    * read
    * validate
      * == watch requests -- to -- reload the configuration 
    * apply
    
* [ALL configuration settings](/prometheus/docs/configuration/configuration.md)

### Configuration reading and parsing

* | load initial configuration OR subsequent reload happens,
  * Prometheus calls the [`config.LoadFile()`](/prometheus/config/config.go#L52-L64) function /
    * read its configuration -- from a -- file
    * parse it | [`config.Config` structure](/prometheus/config/config.go#L133-L145)
    * validate it
    * return `config.Config`

* `type config.Config struct`
  * == 💡Prometheus's config fileS's top-level💡
    * _Examples:_ `GlobalConfig`, `RuntimeConfig`, `StorageConfig`, `OTLPConfig`, ...
    * EACH one has
      * default configuration
        * _Examples:_
          * `Config`  --  `DefaultConfig`
          * `GlobalConfig`  --  `DefaultGlobalConfig`
          * `RuntimeConfig`  --  `DefaultRuntimeConfig`
          * ...
      * `.UnmarshalYAML()`
        * == method / 
          * FROM YAML, parses the struct
          * may apply further validity checks OR initializations

## Reload handler

* [reload handler's configuration](https://github.com/prometheus/prometheus/blob/v2.3.1/cmd/prometheus/main.go#L443-L478)
  * == goroutine / 
    * implemented | `main()`
    * 👀listens for configuration reload requests👀 -- from -- 
      * web interface OR 
      * [`HUP` signal](https://en.wikipedia.org/wiki/Signal_(IPC)#SIGHUP)
    * | receive a reload request,
      * it re-reads the configuration file -- , via `config.LoadFile()`, from -- disk

## Termination handler

* [termination handler's configuration](https://github.com/prometheus/prometheus/blob/v2.3.1/cmd/prometheus/main.go#L367-L392)
  * == goroutine / 
    * implemented | `main()`
    * 👀listens for termination requests👀-- from --
      * web interface OR
      * [`TERM` signal](https://en.wikipedia.org/wiki/Signal_(IPC)#SIGTERM)
    * | receive a termination request,
      * returns & triggers -- , via actor coordination, -- the ORDERLY shutdown of ALL OTHER Prometheus components

## Scrape discovery manager

* scrape discovery manager
  * == [`discovery.Manager`](/prometheus/discovery/manager.go) / 
    * about list of targets | Prometheus should scrape metrics -- , via Prometheus's service discovery functionality, --
    * CONTINUOUSLY find    
    * CONTINUOUSLY update 
  * runs 
    * INDEPENDENTLY of the [scrape manager](#scrape-manager)
    * 1 instance / EACH configuration-defined service discovery mechanism | its OWN goroutine
  * feeds -- , via [synchronization channel](https://github.com/prometheus/prometheus/blob/v2.3.1/cmd/prometheus/main.go#L431), -- the [scrape manager](#scrape-manager)
    * with a stream of updated [target group](https://github.com/prometheus/prometheus/blob/v2.3.1/discovery/targetgroup/targetgroup.go#L24-L33)

* TODO:
* For example, if a `scrape_config` in the configuration file defines two [`kubernetes_sd_config` sections](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config), 
* the manager will run two separate [`kubernetes.Discovery`](https://github.com/prometheus/prometheus/blob/v2.3.1/discovery/kubernetes/kubernetes.go#L150-L159) instances
* Each of these discovery instances implements the [`discovery.Discoverer` interface](https://github.com/prometheus/prometheus/blob/v2.3.1/discovery/manager.go#L41-L55) and sends target updates over a synchronization channel to the controlling discovery manager, which then enriches the target group update with information about the specific discovery instance and forwards it to the scrape manager.

When a configuration change is applied, the discovery manager stops all currently running discovery mechanisms and restarts new ones as defined in the new configuration file.

* [MORE](../discovery/README.md)

## Scrape manager

The scrape manager is a [`scrape.Manager`](https://github.com/prometheus/prometheus/blob/v2.3.1/scrape/manager.go#L47-L62) that is 
responsible for scraping metrics from discovered monitoring targets and forwarding the resulting samples to the storage subsystem.

(which performs the actual target scrapes)

### Target updates and overall architecture

In the same way that the scrape discovery manager runs one discovery mechanism for each `scrape_config`, the scrape manager runs a corresponding scrape pool for each such section. Both identify these sections (e.g. across reloads and across the two components) via the section's `job_name` field, which has to be unique in a given configuration file. The discovery manager sends target updates for each `scrape_config` over a synchronization channel to the scrape manager, [which then applies those updates to the corresponding scrape pools](https://github.com/prometheus/prometheus/blob/v2.3.1/scrape/manager.go#L150-L173). Each scrape pool in turn runs one scrape loop for each target. The overall hierarchy looks like this:

* Scrape manager
  * Scrape pool for `scrape_config` 1
    * Scrape loop for target 1
    * Scrape loop for target 2
    * Scrape loop for target 3
    * [...]
    * Scrape loop for target n
  * Scrape pool for `scrape_config` 2
    * [...]
  * Scrape pool for `scrape_config` 3
    * [...]
  * [...]
  * Scrape pool for `scrape_config` n
    * [...]

### Target labels and target relabeling

Whenever the scrape manager receives an updated list of targets for a given scrape pool from the discovery manager, the scrape pool applies default target labels (such as `job` and `instance`) to each target and applies [target relabeling configurations](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config) to produce the final list of targets to be scraped.

### Target hashing and scrape timing

To spread out scrapes within a scrape pool and in a consistently slotted way across the `scrape_config`'s scrape interval, each target is [hashed by its label set and its final scrape URL](https://github.com/prometheus/prometheus/blob/v2.3.1/scrape/target.go#L75-L82). This hash is then used to [choose a deterministic offset](https://github.com/prometheus/prometheus/blob/v2.3.1/scrape/target.go#L84-L98) within that interval.

### Target scrapes

Finally, a scrape loop periodically scrapes its targets over HTTP and tries to decode the received HTTP responses according to the [Prometheus text-based metrics exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/). It then applies [metric relabeling configurations](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#%3Cmetric_relabel_configs%3E) to each individual sample and sends the resulting samples to the storage subsystem. Additionally, it tracks and stores the staleness of time series over multiple scrape runs, records [scrape health information](https://prometheus.io/docs/concepts/jobs_instances/#automatically-generated-labels-and-time-series) (such as the `up` and `scrape_duration_seconds` metrics), and performs other housekeeping tasks to optimize the appending of time series to the storage engine. Note that a scrape is not allowed to take longer than the configured scrape interval, and the configurable scrape timeout is capped to that. This ensures that one scrape is terminated before another one begins.

## Storage

Prometheus stores time series samples in a local time series database (TSDB) and optionally also forwards a copy of all samples to a set of configurable remote endpoints. Similarly, Prometheus reads data from the local TSDB and optionally also from remote endpoints. Both local and remote storage subsystems are explained below.

### Fanout storage

The [fanout storage](https://github.com/prometheus/prometheus/blob/v2.3.1/storage/fanout.go#L27-L32) is a [`storage.Storage`](https://github.com/prometheus/prometheus/blob/v2.3.1/storage/interface.go#L31-L44) implementation that proxies and abstracts away the details of the underlying local and remote storage subsystems for use by other components. For reads, it merges query results from local and remote sources, while writes are duplicated to all local and remote destinations. Internally, the fanout storage differentiates between a primary (local) storage and optional secondary (remote) storages, as they have different capabilities for optimized series ingestion.

Currently rules still read and write directly from/to the fanout storage, but this will be changed soon so that rules will only read local data by default. This is to increase the reliability of alerting and recording rules, which should only need short-term data in most cases.

### Local storage

About Prometheus's local on-disk time series database, please refer to [`github.com/prometheus/prometheus/tsdb.DB`](https://github.com/prometheus/prometheus/blob/main/tsdb/db.go). You can find more details about the TSDB's on-disk layout in the [local storage documentation](https://prometheus.io/docs/prometheus/latest/storage/).

### Remote storage

The remote storage is a [`remote.Storage`](https://github.com/prometheus/prometheus/blob/v2.3.1/storage/remote/storage.go#L31-L44) that implements the [`storage.Storage` interface](https://github.com/prometheus/prometheus/blob/v2.3.1/storage/interface.go#L31-L44) and is responsible for interfacing with remote read and write endpoints.

For each [`remote_write`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write) section in the configuration file, the remote storage creates and runs one [`remote.QueueManager`](https://github.com/prometheus/prometheus/blob/v2.3.1/storage/remote/queue_manager.go#L141-L161), which in turn queues and sends samples to a specific remote write endpoint. Each queue manager parallelizes writes to the remote endpoint by running a dynamic number of shards based on current and past load observations. When a configuration reload is applied, all remote storage queues are shut down and new ones are created.

For each [`remote_read`](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read) section in the configuration file, the remote storage creates a [reader client](https://github.com/prometheus/prometheus/blob/v2.3.1/storage/remote/storage.go#L96-L118) and results from each remote source are merged.

## PromQL engine

The [PromQL engine](https://github.com/prometheus/prometheus/blob/v2.3.1/promql/engine.go#L164-L171) is responsible for evaluating [PromQL expression queries](https://prometheus.io/docs/prometheus/latest/querying/basics/) against Prometheus's time series database. The engine does not run as its own actor goroutine, but is used as a library from the web interface and the rule manager. PromQL evaluation happens in multiple phases: when a query is created, its expression is parsed into an abstract syntax tree and results in an executable query. The subsequent execution phase first looks up and creates iterators for the necessary time series from the underlying storage. It then evaluates the PromQL expression on the iterators. Actual time series bulk data retrieval happens lazily during evaluation (at least in the case of the local TSDB). Expression evaluation returns a PromQL expression type, which most commonly is an instant vector or range vector of time series.

## Rule manager

The rule manager is a [`rules.Manager`](https://github.com/prometheus/prometheus/blob/v2.3.1/rules/manager.go#L410-L418) that is responsible for evaluating recording and alerting rules on a periodic basis (as configured using the `evaluation_interval` configuration file setting). It evaluates all rules on every iteration using PromQL and writes the resulting time series back into the storage.

For alerting rules, the rule manager performs several actions on every iteration:

- It stores the series `ALERTS{alertname="<alertname>", <alert labels>}` for any pending or firing alerts.
- It tracks the lifecycle state of active alerts to decide when to transition an alert from pending to firing (depending on the `for` duration in the alerting rule).
- It expands the label and annotation templates from the alerting rule for each active alert.
- It sends firing alerts to the notifier (see below) and keeps sending resolved alerts for 15 minutes.

## Notifier

The notifier is a [`notifier.Manager`](https://github.com/prometheus/prometheus/blob/v2.3.1/notifier/notifier.go#L104-L119) that takes alerts generated by the rule manager via its `Send()` method, enqueues them, and forwards them to all configured Alertmanager instances. The notifier serves to decouple generation of alerts from dispatching them to Alertmanager (which may fail or take time).

## Notifier discovery

* notifier discovery manager
  * == [`discovery.Manager`](https://github.com/prometheus/prometheus/blob/v2.3.1/discovery/manager.go#L73-L89)
  * uses
    * Prometheus's service discovery functionality can find & continuously update the list of Alertmanager instances / notifier should send alerts to
  * runs INDEPENDENTLY of the notifier manager
  * feeds the notifier manager -- , over a [synchronization channel](https://github.com/prometheus/prometheus/blob/v2.3.1/cmd/prometheus/main.go#L587), with a -- stream of target group updates 

* 's works
  * == scrape discovery manager's work

## Web UI and API

Prometheus serves its web UI and API on port `9090` by default
* The web UI is available at `/` and serves a human-usable interface for running expression queries, inspecting active alerts, or getting other insight into the status of the Prometheus server.

The web API is served under `/api/v1` and allows programmatic [querying, metadata, and server status inspection](https://prometheus.io/docs/prometheus/latest/querying/api/).

[Console templates](https://prometheus.io/docs/visualization/consoles/), which allow Prometheus to serve user-defined HTML templates that have access to TSDB data, are served under `/consoles` when console templates are present and configured.
