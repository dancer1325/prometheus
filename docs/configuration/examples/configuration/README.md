* goal
  * types of configurations
  * 

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
  * uncomment "prometheusFileBased.yml"'s line
    * Problems:
      * Problem1: Why hot-reload is not happening?
        * Solution: TODO:

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

* _Example:_ [here](/prometheus/config/testdata/conf.good.yml)

* `global`'s parameters applied | ALL OTHER configurations' sections
  * | root path,
    * `prometheus --config.file=config/testdata/conf.good.yml --web.listen-address=:9090`
  * | browser, http://localhost:9090/service-discovery
    * check the labels -- _Example:_ `scrape_interval`

* TODO:
