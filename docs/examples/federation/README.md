* goal
  * hierarchichal federated Prometheus
  * cross-service federated Prometheus

# requirements
* install [Prometheus & Promtool](/prometheus/README.md#install)
* `make assets`

# how to run locally?
## hierarchichal federated Prometheus
* | root path,
  * TODO:

## cross-service federated Prometheus
* | root path,
  * TODO:

## `/federate` endpoint
* ways
  * -- via -- Docker
  * -- via -- `prometheus`

### -- via -- Docker
* | this path,
  * `docker compose -f docker-compose.yml`
* hit [federate requests](federate-endpoint-examples.http) 

### -- via -- `prometheus`
* | root path,
    * `prometheus --config.file=docs/examples/federation/federate-endpoint-prometheus.yml --web.listen-address=:9090`
* hit [federate requests](federate-endpoint-examples.http)

