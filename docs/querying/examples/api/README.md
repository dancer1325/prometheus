* goal

* | browser,
  * http://localhost:9090/api/v1
    * NOT exist page
      * Reason:🧠ONLY the Prometheus server's host🧠

# Format overview
* hit [sample.http](sample.http)

# Expression queries
* hit [sampleExpressionQueries.http](sampleExpressionQueries.http)
## Instant queries
* evaluated | 1! instant
  * check API's response `value`

* `?query=<string>` /
  * `<string>` == PromQL expression
## Range queries
