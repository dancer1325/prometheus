* goal
  *

# PromQL

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
    * `{__name__=~".+"}`
      * check ALL supported metrics

## instant query
* | table

## range query
* | graph

# Expression language data types

## instant vector

* | browser,
  * http://localhost:9090/query, | table
    * `http_requests_total`
      * check returned expressions structure
        * ❌NOT contain @timestamp❌
          * Reason:🧠redundant == the one | you are querying🧠

## range vector

* | browser,
  * http://localhost:9090/query, | table
    * `http_requests_total[5m]`
      * check returned expressions structure
        * contain @timestamp

## scalar

* | browser,
  * http://localhost:9090/query, | table
    * `http_requests_total * 100`

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

