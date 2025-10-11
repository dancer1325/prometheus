# Remote storage adapter

* goal
  * write adapter /
    * receives samples -- via -- Prometheus's remote write protocol
    * store the samples | Graphite, InfluxDB, or OpenTSDB
  * read adapter /
    * read back data through Prometheus -- via -- Prometheus's remote read protocol
    * enabled | InfluxDB 

## steps 
* | this path
  * `go build`
    * build
  * if you want to run
    * Graphite -> `./remote_storage_adapter --graphite-address=localhost:8080`
    * OpenTSDB -> `./remote_storage_adapter --opentsdb-url=http://localhost:8081/`
    * InfluxDB -> `INFLUXDB_AUTH_TOKEN=<token> ./remote_storage_adapter --influxdb-url=http://localhost:8086/ --influxdb.organization=<organization_name> --influxdb.bucket=<bucket_name>`
  * `docker compose up -d`

* TODO: check
