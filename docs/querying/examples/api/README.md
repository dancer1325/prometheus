* goal

* | browser,
  * http://localhost:9090/api/v1
    * NOT exist page
      * Reason:🧠ONLY the Prometheus server's host🧠

* hit [sample.http](sample.http)

# Format overview
* hit [sampleFormatOverview.http](sampleFormatOverview.http)

# Expression queries
* hit [sampleExpressionQueries.http](sampleExpressionQueries.http)
## Instant queries
* evaluated | 1! instant
  * check API's response `value`

* `?query=<string>` /
  * `<string>` == PromQL expression
## Range queries
* evaluated | range of time
  * check API's URL parameters `start` & `end`

# TODO:

# Expression query result formats
* hit [sampleExpressionQueryFormats.http](sampleExpressionQueryFormats.http)

# TODO:
