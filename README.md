![](documentation/images/prometheus-logo.svg)

## Prometheus Overview

* == [Cloud Native Computing Foundation](https://cncf.io/) project
* == Systems & service monitoring system /
  * responsible for
    * collecting metrics | intervals
      * -- by scraping -- HTTP endpoints
    * evaluates rules
    * displays results
    * triggers alerts

* features
  * **Multi-dimensional data model**
    * Multi-dimensional == ALL labels
  * **PromQL**
    * == query language
      * powerful
      * flexible 
  * **Autonomous nodes**
    * != distributed storage dependency
    * ⚠️== EACH Prometheus instance work INDEPENDENTLY⚠️
    * cons
      * complex configuration & maintenance
  * **HTTP pull model** 
    * -- for -- time series collection
  * **Push support**
    * -- via -- intermediary Pushgateway
    * use cases
      * batch jobs
        * Reason: 🧠batch jobs
          * NOT provide endpoint / scrape
          * complete & die🧠
  * **Target discovery**
    * allows
      * finding services / monitor
    * types
      * [service discovery](#service-discovery-plugins)
        * == dynamic
          * _Example:_ Kubernetes scaling, AWS Autoscaling
      * static configuration
  * **Graphing & dashboards**
    * supported
      * Prometheus Web UI
      * Grafana
      * Tableau
      * ...
  * **Federation**
    * == MULTIPLE Prometheus instances / hierarchical

* architecture overview

  ![Architecture overview](documentation/images/architecture.svg)

## Install

### Precompiled binaries

* [download](https://prometheus.io/download/)
  * choose different prometheus components

### Docker images

* hosted |
  * [Quay.io](https://quay.io/repository/prometheus/prometheus)
  * [Docker Hub](https://hub.docker.com/r/prom/prometheus/)

* steps
  * | any terminal,
    * `docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus`
  * | browser.
    * http://localhost:9090/
  * check prometheus server
    * `docker exec -it prometheus sh`
    * `prometheus --help`

### Building from source

* requirements
  * Go OR make
    * Go \>= version specified | [go.mod](./go.mod)
  * NodeJS
    * \>= version specified | [.nvmrc](./web/ui/.nvmrc)
  * npm v8+

* goal
  * ⚠️ONLY the binary⚠️
    * -> ❌[sample prometheus.yml](https://github.com/dancer1325/prometheus-website/blob/main/docs/introduction/first_steps.md#configuring-prometheus) NOT included❌

#### how to build a Docker image?

* | this terminal
  * `make promu`
    * Problems:
      * Problem1: "make: Nothing to be done for `promu'"
        * Solution: TODO:
  * `promu crossbuild -p linux/amd64`
  * `make npm_licenses`
  * `make common-docker-amd64`

#### Go

* ❌NOT include the React UI❌
  * 💡if you want to use it -> `make assets` 💡

* steps
  * | ⚠️this path⚠️,

    ```bash
    GO111MODULE=on go install github.com/prometheus/prometheus/cmd/...
    # GO111MODULE=on      == enable Go modules  (| Go 1.16+, ALREADY included)
    # build & install the `prometheus` & `promtool` binaries | your `GOPATH`
    # ...     == install ALL subdirectories 
    
    prometheus --config.file=your_config.yml
    # prometheus --config.file=documentation/examples/prometheus.yml
    ```
    * Problems: 
      * Problem1: | `go install ...`, "...403 Forbidden"
        * Solution: `go install ./cmd/prometheus ./cmd/promtool`
    * [cmd](cmd)
      * == prometheus + promtool
    * ❌if you do NOT run | this path -> fail❌
      * Reason: 🧠
        * Prometheus expect to read its web assets | local filesystem directories "web/ui/static" & "web/ui/templates"
          * OTHERWISE, NOT found🧠
    * installed | 👀"{go env GOPATH}/bin"👀
      * NORMALLY, "$HOME/go/bin"
    * _Example of configurations:_ [here](documentation/examples/prometheus.yml)
  * check prometheus server
    * `prometheus --help`

#### make

* steps
  * | this path,

      ```bash
      make build        # compile & include web assets | Prometheus binary 
    
      ./prometheus --config.file=your_config.yml
      ```

* Makefile
  * provided targets
    * *build*
      * build the `prometheus` & `promtool` binaries + build & compile | web assets
    * *test*
      * run the tests
    * *test-short*
      * run the short tests
    * *format*
      * format the source code
    * *vet*
      * check the source code / COMMON errors
    * *assets*
      * build the React UI

### Service discovery plugins

* [plugins.yml](./plugins.yml)
  * == go import path /
    * yaml-formatted
  * uses
    * build | Prometheus binary
      * if some does NOT want to be used -> steps 
        * disable it
        * `make build` OR `make plugins`

* [MORE](discovery/README.md)

## Using Prometheus as a Go Library

### Remote Write

* TODO: We are publishing our Remote Write protobuf independently at
[buf.build](https://buf.build/prometheus/prometheus/assets).

You can use that as a library:

```shell
go get buf.build/gen/go/prometheus/prometheus/protocolbuffers/go@latest
```

This is experimental.

### Prometheus code base

In order to comply with [go mod](https://go.dev/ref/mod#versions) rules,
Prometheus release number do not exactly match Go module releases.

For the
Prometheus v3.y.z releases, we are publishing equivalent v0.3y.z tags
* The y in v0.3y.z is always padded to two digits, with a leading zero if needed.

Therefore, a user that would want to use Prometheus v3.0.0 as a library could do:

```shell
go get github.com/prometheus/prometheus@v0.300.0
```

For the
Prometheus v2.y.z releases, we published the equivalent v0.y.z tags.

Therefore, a user that would want to use Prometheus v2.35.0 as a library could do:

```shell
go get github.com/prometheus/prometheus@v0.35.0
```

This solution makes it clear that we might break our internal Go APIs between
minor user-facing releases, as [breaking changes are allowed in major version
zero](https://semver.org/#spec-item-4).

## React UI Development

* [here](web/ui/README.md)

## Community

* [Community](https://prometheus.io/community)
