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
* [prometheusScrapeConfigOneUniqueJob.yml](prometheusScrapeConfigOneUniqueJob.yml)
* `docker compose up -d`
* | browser, http://localhost:9090/targets
    * check ALL defined targets
### >1 target groups / 1 job
* [prometheusScrapeConfigSeveralTargetGroupsPerJob.yml](prometheusScrapeConfigSeveralTargetGroupsPerJob.yml)
* `docker compose up -d`
* | browser, http://localhost:9090/targets
    * check ALL defined targets & target groups
### `job_name`
* [prometheusJobName.yml](prometheusJobName.yml)
* `docker compose up -d`
* | browser, http://localhost:9090/targets
  * check ALL defined targets`
### `scrape_interval`
* [prometheusScrapeConfigScrapeInterval.yml](prometheusScrapeConfigScrapeInterval.yml)
* `docker compose up -d`
* http://localhost:9090/targets
  * refresh checking LAST time of scrape
### `scrape_timeout`
* [prometheusScrapeConfigScrapeInterval.yml](prometheusScrapeConfigScrapeInterval.yml)
* `docker compose up -d`
* http://localhost:9090/targets
  * refresh checking LAST time of scrape
  * | 8s,
    * target is down
### `scrape_protocols`
* [prometheusScrapeConfigScrapeProtocols.yml](prometheusScrapeConfigScrapeProtocols.yml)
* `docker compose up -d`
* http://localhost:9090/targets
  * refresh checking LAST time of scrape
* http://localhost:9090/query
  * `scrape_duration_seconds`
    * check DIFFERENT samples -- based on -- scrape protocol
### `fallback_scrape_protocol`
* `python3 brokenExporter.py`
* [prometheusScrapeConfigFallbackScrapeProtocol.yml](prometheusScrapeConfigFallbackScrapeProtocol.yml)
* `docker compose up -d`
* http://localhost:9090/targets
  * ERROR | scrape localhost:9999  

### configure target / DYNAMICALLY
#### `file_sd_configs`
* [prometheusFileServiceDiscovery.yml](prometheusFileServiceDiscovery.yml)
* see [targets](targets)
* `docker compose up -d`
* | browser, 
  * http://localhost:9090/targets
    * check ALL defined targets & target groups
  * http://localhost:9090/service-discovery
    * check ALL service discoveries
#### `<http_sd_config>`
* [prometheusHTTPServiceDiscovery.yml](prometheusHTTPServiceDiscovery.yml)
* `python3 http-sd-server.py`
* `docker compose up -d`
* | browser,
  * http://localhost:9090/targets
    * check ALL defined targets & target groups
  * http://localhost:9090/service-discovery
    * `__meta_url` 
      * appear
