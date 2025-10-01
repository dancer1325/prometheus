* goal
  * types of configurations

# requirements

* install [Prometheus & Promtool](/prometheus/README.md#install)
* `make assets`

# types of configurations

* steps
  * | root path,
    * `prometheus --config.file=docs/configuration/examples/configuration/prometheusFileBased.yml --web.listen-address=:9090 --web.enable-lifecycle`
      * `--config.file` & `--web.listen-address`
        * == flag-based configuration
      * "docs/configuration/examples/configuration/prometheusFileBased.yml"
        * == file-based configuration

* reload Prometheus rule | runtime
  * ❌BUT NOT AUTOMATICALLY❌
    * steps
      * uncomment lines
      * check NOTHING is modified
  * ways to trigger
    * `-HUP` signal
      * steps
        * | RANDOM path,
          * `ps aux | grep prometheus`
          * `kill -HUP PREVIOUS_PID_GOT`
        * | browser, "http://localhost:9090/targets"
          * check appear
    * hit "/reload"
      * `curl -X POST http://localhost:9090/-/reload`

# configuration file

* `global`'s parameters applied | ALL OTHER configurations' sections
  * | root path,
    * `prometheus --config.file=config/testdata/conf.good.yml --web.listen-address=:9090`
  * | browser, http://localhost:9090/service-discovery
    * check the labels -- _Example:_ `scrape_interval`

* _Example of generic placeholders:_ [prometheusGenericPlaceHolders.yml](prometheusGenericPlaceHolders.yml)

## `scrape_config`
### 1! job / 1 scrape configuration
* `docker compose up -d`
* | browser, http://localhost:9090/targets
  * check ALL defined targets
### >1 target groups / 1 job
* `docker compose up -d`
* | browser, http://localhost:9090/targets
    * check ALL defined targets & target groups
### configure target / DYNAMICALLY
#### `file_sd_configs`
* see [targets](targets)
* `docker compose up -d`
* | browser, 
  * http://localhost:9090/targets
    * check ALL defined targets & target groups
  * http://localhost:9090/service-discovery
    * check ALL service discoveries



* | [database-targets.yml](targets/database-targets.yml),
  * uncomment the line
  * `ps aux | grep prometheus`
  * `kill -HUP PREVIOUS_PID_GOT`
  * | browser,
    * http://localhost:9090/targets
      * check NEW label added


* TODO:
