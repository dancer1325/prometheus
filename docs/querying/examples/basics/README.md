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

# PromQL's supported expressions
## Literals
### string literals
#### escaping rules
##### ignored | Prometheus UI
* | browser,
  * http://localhost:9090/query
    * 'Hello \n world'
      * NO
    * "Hello \n world"
    * `Hello \n world`
##### API
* hit [sample.http](sample.http)

### float literals and time durations
#### float literals
* | browser,
  * http://localhost:9090/query
 
      ```text
      // literal integer
      23     
      
      // literal floating-point number  
      -2.43
      3.4e-9
      0x8f
      -Inf
      NaN
    
      // decimal
      .123_456_789  
    
      // hexadecimal
      0x_53_AB_F3_82  
    
      // if number is big -> use underscores (`_`)
      1_000_000 
    
      // uses
      // math operations
      go_gc_gogc_percent * 100
      // compare & filters
      prometheus_http_requests_total > 1000      
      ```
#### time durations
* | browser,
  * http://localhost:9090/query

    ```text
    // `integerNumber` + `durationTimeUnit`
    1s # == 1
    
    // ALLOWED time units
    2m # == 120 == 120 s
    1ms # == 0.001
    -2h # == -7200
    
    // if you do NOT specify durationTimeUnit   -> s
    2   # 2
    
    # if you do NOT specify integer numbers -> NOT valid 
    0xABm   # No suffixing of hexadecimal numbers
    1.5h    # Time units cannot be combined with a floating point.
    +Infd   # No suffixing of ±Inf or NaN.
  
    # concatenated
    1h30m           # == 5400s == 5400
    12h34m56s       # == 45296s == 45296
    54s321ms        # == 54.321
    30m1h           # WRONGLY concatenated -> NOT valid
    
    # uses
    # 1. range vectors
    rate(prometheus_http_requests_total[5m])
    # 3. offset modifiers
    prometheus_http_requests_total offset 1h
    ```
## Time series selectors
### Instant vector selectors
#### `metricName`
##### == `{__name__=metricName}`
* | browser,
  * http://localhost:9090/query
    * `prometheus_http_requests_total`
    * `{__name__="prometheus_http_requests_total"}`
##### keywords / NOT ALLOWED
* | browser,
  * http://localhost:9090/query
    * `bool`
    * `on`
    * `ignoring`
    * `group_left`
    * `group_right`
#### selecting a set of time serieS / 1! sample value / EACH time series | given timestamp
* | browser,
  * http://localhost:9090/query
    * `prometheus_http_requests_total`
      * by default, CURRENT
      * adjust timestamp
#### `metricname{label1=value1,label2=value,...}`
* | browser,
  * http://localhost:9090/query
    * `prometheus_http_requests_total{handler="/-/healthy"}`
#### ways to match label vs value
##### operators
###### `=`
* `prometheus_http_requests_total{handler="/-/healthy"}`
* ❌NOT valid❌
  * `prometheus_http_requests_total{code="400|404|302"}`
    * Reason:🧠regular expression🧠
###### `!=`
* `prometheus_http_requests_total{handler!="/-/healthy"}`
###### `=~`
* `prometheus_http_requests_total{code=~"200|400|404|302"}`
* `prometheus_http_requests_total{code=~"400|404|302"}`
* `prometheus_http_requests_total{code=~"404|302"}`
###### !~
* `prometheus_http_requests_total{code!~"200|400"}`
##### EMPTY label value
* `prometheus_http_requests_total{version=""}`
  * `version` label does NOT exist -> return ALL
##### MULTIPLE matchers | SAME label name
* `prometheus_http_requests_total{code!="200",code!="400"}`
  * == `prometheus_http_requests_total{code!~"200|400"}`
#### specify `metricName` OR ( label matcher / NOT EMPTY string value)
* `{job=""}`
  * ERROR
* `{job=~".*"}`
  * ERROR
    * Reason:🧠
      * `.` == ANY character
      * `*` >= 0 strings🧠
* `{job=~".+"}`
  * FINE
    * Reason:🧠`+` >= 1 strings🧠
### Range vector selectors
#### `metricName[floatLiteral]`
* `prometheus_http_requests_total[5m]`
#### `metricName{label1="value1",label2="value2",...}[floatLiteral]`
* `prometheus_http_requests_total{code="404"}[5m]`
### Offset modifier
#### ❌| instant vector selector, NOT valid❌
* `prometheus_http_requests_total offset 20m`
  * ALWAYS return | CURRENT or GIVEN timestamps
#### if `offset` NOT IMMEDIATELY AFTER selector -> NOT valid
* `sum(prometheus_http_requests_total[5m]) offset 20m`
  * ❌NOT valid❌
#### past
* `prometheus_http_requests_total[5m] offset 20m`
  * `prometheus_http_requests_total[5m]` 20m ago
#### future
* http://localhost:9090/query
  * ⚠️adjust the time | evaluate⚠️
  * `prometheus_http_requests_total[5m] offset -20m`
    * `prometheus_http_requests_total[5m]` -20m ago | GIVEN timestamp
### @ modifier
#### ❌`instantVectorSelector @ timestampAsFloatLiteral` NOT valid❌
* `prometheus_http_requests_total @ 1759662516`
  * ALWAYS return CURRENT or GIVEN time
    * -- via -- [API](sample.http)
    * -- via -- UI
#### `rangeVectorSelector @ timestampAsFloatLiteral`
* `prometheus_http_requests_total[5m] @ 1759662516`
#### ❌if `@` NOT IMMEDIATELY AFTER selector -> NOT valid❌
* `(prometheus_http_requests_total[5m]) @ 1759662516`
### @ modifier + offset modifier  OR  offset modifier + @ modifier
#### `instantVectorSelector @ timestampAsFloatLiteral offset timeDuration`
* `prometheus_http_requests_total @ 1759662516 offset 5m`
  * ❌NOT valid❌
    * ALWAYS return CURRENT or GIVEN time
#### `instantVectorSelector offset timeDuration @ timestampAsFloatLiteral`
* `prometheus_http_requests_total offset 5m @ 1759662516`
  * ❌NOT valid❌
    * ALWAYS return CURRENT or GIVEN time
#### `rangeVectorSelector offset timeDuration @ timestampAsFloatLiteral`
* `prometheus_http_requests_total[5m] offset 5m @ 1759662516`
#### `rangeVectorSelector @ timestampAsFloatLiteral offset timeDuration `
* `prometheus_http_requests_total[5m] @ 1759662516 offset 5m`
### `@ start()` & `@ end()`
* `rate(prometheus_http_requests_total[5m] @ start())`
  * Problems:
    * Problem1: ALWAYS CURRENT or GIVEN timestamp
      * Solution: TODO:
* `rate(prometheus_http_requests_total[5m] @ end())`
  * Problems:
    * Problem1: ALWAYS CURRENT or GIVEN timestamp
      * Solution: TODO:
## Subquery
* `prometheus_http_requests_total[30m:15m]`
  * return a range vector / 2 hits
### <resolution> OPTIONAL
* `prometheus_http_requests_total[30s]`
  * returns 2 hits -- Reason: 🧠`evaluation_interval: 15s` 🧠
## Comments
```
#This is a comment
prometheus_http_requests_total
```

# Regular expression
## FULLY anchored
* `prometheus_http_requests_total{handler=~"/api/v1/admin/tsdb/clean_tombstones"}`
  * == 
    * `prometheus_http_requests_total{handler=~"^/api/v1/admin/tsdb/clean_tombstones"}`
    * `prometheus_http_requests_total{handler=~"/api/v1/admin/tsdb/clean_tombstones$"}`
    * `prometheus_http_requests_total{handler=~"^/api/v1/admin/tsdb/clean_tombstones$"}`
## if you alternate OR concatenate 2 regular expressions -> new regular expression
### alternate -- `e1 | e2` --
* `prometheus_http_requests_total{code=~"400|302"}`
### concatenate -- `e1e2` --
* `prometheus_http_requests_total{handler="/api/v1/query_range"}`
  * `/api/v1/` + `query_range`
## metacharacters
### `.`
* `prometheus_http_requests_total{handler=~"/-/heal.hy"}`
  * match with the existing `prometheus_http_requests_total{handler=~"/-/healthy"}`
#### BUT ONLY 1!
* `prometheus_http_requests_total{handler=~"/."}`
  * Reason: `prometheus_http_requests_total{handler=~"/"}` exist, BUT NOTHING else with 2 characters
### `|`
* `prometheus_http_requests_total{code=~"400|302"}`
### `()`
* `prometheus_http_requests_total{handler=~"/api/v1/(alertmanagers|alerts)"}`
### `[]`
* `prometheus_http_requests_total{code=~"[345]00"}`
* `prometheus_http_requests_total{code=~"[3-5]00"}`
### repetition operators
#### `*`
* `prometheus_http_requests_total{handler=~"/api/v1/admin/.*"}`
  * `.*`
    * ANY character / >= 0 repetitions
* `prometheus_http_requests_total{handler=~"/alertss*"}`
  * `s*`
    * 0 repetitions ALSO
#### `+`
* `prometheus_http_requests_total{handler=~"/alertss+"}`
  * NOT returned data
    * Reason:🧠required at least `/alertss` 🧠
#### `?`
* `prometheus_http_requests_total{handler=~"/alertss?"}`
  * `ss?`
    * 0 OR 1 repetition of s == `s` OR `ss`
#### `{}`
* `prometheus_http_requests_total{code=~"[345]0{2}"}`
### if you want to match -> escape them

# TODO:

