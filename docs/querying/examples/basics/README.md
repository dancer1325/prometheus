# PromQL
* `docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus`
## functional query language
### aggregation
* | browser,
  * http://localhost:9090/query
    * `sum(rate(http_requests_total[5m]))`
### pure
* `rate(http_requests_total[5m])`
  * SAME entry | SAME time -> SAME output
### immutable
* `rate(http_requests_total[5m])`
  * ❌NO modify input data❌
### higher-order functions
* `sum by (job) (rate(http_requests_total[5m]))`
### declarative
* `sum(http_requests_total) by (status_code)`
## lets, about time series data | real time,
### select
* | browser,
  * http://localhost:9090/query
    * `http_requests_total`
    * `{__name__=~".+"}`
      * check ALL supported metrics
### aggregate
* | browser,
  * http://localhost:9090/query
    * `sum(rate(http_requests_total[5m]))`
      * compose functions
    * `rate(http_requests_total[5m])`
      * input data do NOT change
    * `http_requests_total[5m]` WITHOUT changing time
      * pure functions
    * `http_requests_total`
      * == select time series data
    * `sum(http_requests_total)`
      * == aggregate time series data
## `{__name__=~".+"}`
* | browser,
  * http://localhost:9090/query
    * `{__name__=~".+"}`

## Expression queries
### instant query
* | table
#### ALLOWED results
##### instant vector
* `prometheus_http_requests_total`
##### scalar
* `prometheus_http_requests_total * 100`
##### string
* `"hello world"`

### range query
* | graph
#### ALLOWED results
##### instant vector
* `rate(prometheus_http_requests_total[5m])`
##### scalar
* `sum(prometheus_http_requests_total)`

# Expression language data types

## instant vector
* | browser,
  * http://localhost:9090/query, | table
    * `prometheus_http_requests_total`
      * check returned expressions structure
        * ❌NOT contain @timestamp❌
          * Reason:🧠redundant == the one | you are querying🧠
### if native histograms ingested | TSDB
* TODO:

## range vector
* | browser,
  * http://localhost:9090/query, | table
    * `prometheus_http_requests_total[5m]`
      * check returned expressions structure
        * contain @timestamp
### if native histograms ingested | TSDB
* TODO:

## scalar
* | browser,
  * http://localhost:9090/query, | table
    * `prometheus_http_requests_total * 100`

## string
* | browser,
  * http://localhost:9090/query, | table
    * `"hello world"`

# Literals

## string literals

## Float literals and time durations
* _Examples to write scalar float values:_ 
  ```text
  23
  -2.43
  3.4e-9
  0x8f
  -Inf
  NaN
  ```

* _Examples to write decimal OR hexadecimal digits:_

    ```text
    1_000_000
    .123_456_789
    0x_53_AB_F3_82
    ```
* _Examples of durations:_

    ```text
    1s # == 1
    2m # == 120
    1ms # == 0.001
    -2h # == -7200
    
    
    # NOT valid, because you specify NOT integer numbers
    0xABm   # No suffixing of hexadecimal numbers.
    1.5h    # Time units cannot be combined with a floating point.
    +Infd   # No suffixing of ±Inf or NaN.
  
  
    # concatenated
    1h30m           # == 5400s == 5400
    12h34m56s       # == 45296s == 45296
    54s321ms        # == 54.321
    ```


* TODO:

