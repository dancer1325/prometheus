* `docker run --name prometheus -d -p 127.0.0.1:9090:9090 prom/prometheus`

# PrompQL's supported operators
## Unary operator
### scalar
* `5` vs `-5`
* `sum(prometheus_http_requests_total)` vs `-sum(prometheus_http_requests_total)`
### instant vector
* `prometheus_http_requests_total{code="400"}` vs `-prometheus_http_requests_total{code="400"}`
#### if it's a histogram sample
* `prometheus_http_request_duration_seconds` -- histogram --
  * invert
    * `prometheus_http_request_duration_seconds_bucket` vs `-prometheus_http_request_duration_seconds_bucket`
    * `prometheus_http_request_duration_seconds_sum` vs `-prometheus_http_request_duration_seconds_sum`
    * `prometheus_http_request_duration_seconds_count` vs `-prometheus_http_request_duration_seconds_count`
## Binary operators
### Arithmetic binary operators
#### `+`
##### scalar -- & -- scalar
* `5+3`
##### vector -- & -- scalar
###### if vector's sample float
* `prometheus_http_requests_total + 10`
###### if vector's native histogram
* TODO:
##### vector -- & -- vector
* `prometheus_http_requests_total + on(app, handler, instance, job) group_left prometheus_http_request_duration_seconds_count`
#### `-`
##### scalar -- & -- scalar
* `5-3`
##### vector -- & -- scalar
* `prometheus_http_requests_total - 10`
##### vector -- & -- vector
* `prometheus_http_requests_total - on(app, handler, instance, job) group_left prometheus_http_request_duration_seconds_count`
#### `*`
##### scalar -- & -- scalar
* `5*3`
##### vector -- & -- scalar
* `prometheus_http_requests_total * 10`
##### vector -- & -- vector
* `prometheus_http_requests_total * on(app, handler, instance, job) group_left prometheus_http_request_duration_seconds_count`
#### `/`
##### scalar -- & -- scalar
* `5/3`
##### vector -- & -- scalar
* `prometheus_http_requests_total / 10`
##### vector -- & -- vector
* `prometheus_http_requests_total / on(app, handler, instance, job) group_left prometheus_http_request_duration_seconds_count`
#### `%`
##### scalar -- & -- scalar
* `5%3`
##### vector -- & -- scalar
* `prometheus_http_requests_total % 10`
##### vector -- & -- vector
* `prometheus_http_requests_total % on(app, handler, instance, job) group_left prometheus_http_request_duration_seconds_count`
#### `^`
##### scalar -- & -- scalar
* `5^3`
##### vector -- & -- scalar
* `prometheus_http_requests_total ^ 10`
##### vector -- & -- vector
* `prometheus_http_requests_total ^ on(app, handler, instance, job) group_left prometheus_http_request_duration_seconds_count`
#### metric name
##### dropped ALTHOUGH you `on(__name__)`
* `prometheus_http_requests_total + on(app, handler, instance, job, __name__) group_left prometheus_http_request_duration_seconds_count`
  * Problem:
    * Problem1:Empty query result. This query returned no data.
      * Solution: `prometheus_http_requests_total + on(app, handler, instance, job) group_left prometheus_http_request_duration_seconds_count`

### Trigonometric binary operators
* `prometheus_tsdb_head_series atan2 prometheus_tsdb_head_samples_appended_total`
  * `prometheus_tsdb_head_series{app="prometheus", instance="localhost:9090", job="prometheus"}`
  * `prometheus_tsdb_head_samples_appended_total{instance, job, type}`
  * Problems:
    * Problem1: "NOT return data"
      * Reason: NO vector matching BETWEEN left side & right side
      * Attempt1: `prometheus_tsdb_head_series atan2 on(instance,job) prometheus_tsdb_head_samples_appended_total`
      * Solution: `prometheus_tsdb_head_series atan2 on(instance, job) prometheus_tsdb_head_samples_appended_total{type="float"}`

### Comparison binary operators
#### `==`
##### scalar/scalar
* `5 == 3`
  * ❌NOT work❌
  * Solution: 💡5 == bool 3💡
##### vector/scalar
* `up == 1`
##### vector/vector
* `up == prometheus_ready`
#### `!=`
##### scalar/scalar
* `5 != 3`
  * ❌NOT work❌
  * Solution: 💡5 == bool 3💡
##### vector/scalar
* `up != 1`
##### vector/vector
* `prometheus_tsdb_head_series != prometheus_tsdb_head_chunks`
#### `>`
##### scalar/scalar
* `5 > 3`
  * ❌NOT work❌
  * Solution: 💡5 == bool 3💡
##### vector/scalar
* `up > 1`
##### vector/vector
* `up > prometheus_ready`
#### `<`
##### scalar/scalar
* `5 < 3`
  * ❌NOT work❌
  * Solution: 💡5 == bool 3💡
##### vector/scalar
* `up < 1`
##### vector/vector
* `up < prometheus_http_requests_total`
#### `>=`
##### scalar/scalar
* `5 >= 3`
  * ❌NOT work❌
  * Solution: 💡5 == bool 3💡
##### vector/scalar
* `up >= 1`
##### vector/vector
* `up >= prometheus_ready`
#### `<=`
##### scalar/scalar
* `5 <= 3`
  * ❌NOT work❌
  * Solution: 💡5 == bool 3💡
##### vector/scalar
* `up <= 1`
##### vector/vector
* `up <= prometheus_ready`

#### vector/scalar
##### if vector's sample == histogram -> corresponding result vector's element is removed
* TODO:
##### if vector elements comparison is false -> dropped from the result vector
* TODO:

#### matching
##### float sample & histogram sample invalid
* TODO:
##### 2 histogram samples
###### valid
* `==`
  * TODO:
* `!=`
  * TODO:
###### NOT valid
* `>`
  * TODO:
* `>=`
  * TODO:
* `<`
  * TODO:
* `<=`
  * TODO:

#### `bool`
##### if vector | SOME side -> metric name is dropped
* `up == prometheus_ready`
  * returns ALSO metricName
  * `up == bool prometheus_ready`
    * ❌NOT return metricName❌
##### if vectorS comparison / match & expression false & use bool -> return 1
* `up > prometheus_ready`
  * returns "Empty query result. This query returned no data."
  * `up > bool prometheus_ready`
    * return samples ALTHOUGH 0

#### metric name
##### if `on` is used -> it's dropped
* `up == prometheus_ready`
  * return include metric name
* `up == on(instance, job) prometheus_ready`
  * return NOT include metric name
##### if `group_right` OR `group_left` is used -> right side's OR left side's metric name
* `prometheus_http_requests_total == on(handler, instance, job) prometheus_http_request_duration_seconds_count`
  * NOT return metric name
* `prometheus_http_requests_total == on(handler, instance, job) group_left prometheus_http_request_duration_seconds_count`
  * return left side's metric name

### Logical/set binary operators
#### `and`
##### `vector1`'s elements == `vector2`'s elements / EXACTLY match label sets
###### float samples
* `up and prometheus_ready`
  * `up{instance, job}`
  * `prometheus_ready{instance, job}`
* `up and prometheus_engine_query_duration_seconds`
  * ❌NOT return anything❌
    * Reason:🧠NOT match labels🧠
###### histogram samples
* TODO:
##### return vector / 's metric name == left side's metric name & 's values == left side's values
* `up and prometheus_ready`
  * return `up{instance, job}`

* TODO:
#### `or`
##### ALL `vector1`'s original elements + ALL `vector2`'s elements / NOT have `vector1`'s matching label sets
###### float samples
* `prometheus_http_requests_total{code="400"} or prometheus_http_request_duration_seconds_count`
  * `prometheus_http_requests_total{app, code, handler, instance, job}`
  * `prometheus_http_request_duration_seconds_count{handler}`
  * NOT match EXACTLY the labels
###### histogram samples
* TODO:
#### `unless`
##### `vector1`'s elements / NO `vector2`'s elements EXACTLY matching label sets
###### float samples
* `prometheus_http_requests_total{code="400"} unless prometheus_http_request_duration_seconds_count`
  * NOT match EXACTLY the labels
###### histogram samples
* TODO:

## Aggregation operators
### `sum`
#### `<aggr-op> [without|by (<label list>)] ([parameter,] <vector expression>)`
* `sum without(job) (up)`
* `sum by(instance) (up)`
* TODO: histogram samples
#### <aggr-op>([parameter,] <vector expression>) [without|by (<label list>)]
* `sum (up) without(job)`
* `sum (up) by(instance)`
* TODO: histogram samples

### `avg(v)`
#### `<aggr-op> [without|by (<label list>)] ([parameter,] <vector expression>)`
* `avg without(job) (up)`
* `avg by(instance) (up)`
* TODO: histogram samples
#### <aggr-op>([parameter,] <vector expression>) [without|by (<label list>)]
* `avg (up) without(job)`
* `avg (up) by(instance)`
* TODO: histogram samples
#### `<aggr-op> [without|by (<label list>)] ([parameter,] <vector expression>)`
* `sum without(job) (up)`
* `sum by(instance) (up)`
* TODO: histogram samples
#### <aggr-op>([parameter,] <vector expression>) [without|by (<label list>)]
* `sum (up) without(job)`
* `sum (up) by(instance)`
* TODO: histogram samples

### `min(v)` & `max(v)`
#### `<aggr-op> [without|by (<label list>)] ([parameter,] <vector expression>)`
* `max without(job) (prometheus_http_requests_total)` vs `max by(job) (prometheus_http_requests_total)`
  * 's return COMPLETELY DIFFERENT
* `min without(job) (prometheus_http_requests_total)` vs `min by(job) (prometheus_http_requests_total)`
  * 's return COMPLETELY DIFFERENT
* TODO: histogram samples
#### <aggr-op>([parameter,] <vector expression>) [without|by (<label list>)]
* `max (prometheus_http_requests_total) without(job) ` vs `max (prometheus_http_requests_total) by(job)`
  * 's return COMPLETELY DIFFERENT
* `min (prometheus_http_requests_total) without(job)` vs `min (prometheus_http_requests_total) by(job)`
  * 's return COMPLETELY DIFFERENT
* TODO: histogram samples

### `bottomk(k, v)` & `topk(k, v)` 
#### 's return vector / contains the original labels
* `topk(3, prometheus_http_requests_total)` OR `bottomk(3, prometheus_http_requests_total)`
#### `by` & `without` bucket `v`
* `topk(1, prometheus_http_requests_total) by (job)` OR `bottomk(1, prometheus_http_requests_total) by (job)` 
  * bucket top or bottom `prometheus_http_requests_total` by `job`
* `topk(1, prometheus_http_requests_total) without (code, handler, instance)` OR `bottomk(1, prometheus_http_requests_total) without (code, handler, instance)`
  * bucket top OR bottom `prometheus_http_requests_total` excluding `code, handler, instance`
#### ❌NO guarantee / buckets of series are returned | any particular order❌
* `topk(2, prometheus_http_requests_total) without (code, instance)`

### `limitk(k, v)`
* `limitk(3, prometheus_http_requests_total)`

### `limit_ratio(r, v)`
* `limit_ratio(0.2, up)`
  * 's return
    * 20% of `up` samples
* `limit_ratio(-0.5, prometheus_http_requests_total)` vs `limit_ratio(0.5, prometheus_http_requests_total)`
  * complementary
    * == ALL samples got -- via -- `prometheus_http_requests_total`

### `group(v)`
* `group(prometheus_http_requests_total)`
  * == 1
    * Reason:🧠grouping ALL WITHOUT filtering in by label🧠
* `group(prometheus_http_requests_total) by(handler)`
  * == 1 / EACH handler sample
* `group(prometheus_http_requests_total) without(handler)`
  * == 1 / excluding handler label

### `count(v)`
* `count(prometheus_http_requests_total)`

### `count_values(l, v)`
* `count_values("handler", prometheus_http_requests_total)`
  * label's name == `handler="itsValue"`

### `stddev(v)`
* `stddev(prometheus_http_requests_total)`

### `stdvar(v)`
* `stdvar(prometheus_http_requests_total)`

### `quantile(φ, v)`
* `quantile(0.5, prometheus_http_requests_total)`
* 

# Vector matching
## Vector matching keywords
### `on`
* `prometheus_http_requests_total + prometheus_http_request_duration_seconds_count`
  * NOT work
    * Reason: 🧠DIFFERENT labels
      * `prometheus_http_requests_total{app, code, handler, instance, job}`
      * `prometheus_http_request_duration_seconds_count{app, handler, instance, job}`🧠
    * Attempt1: `prometheus_http_request_duration_seconds_count + on(app, handler, instance, job) prometheus_http_requests_total`
    * Solution: `prometheus_http_requests_total + on(app, handler, instance, job) group_left prometheus_http_request_duration_seconds_count`

* `prometheus_http_requests_total + on(instance, job) prometheus_http_request_duration_seconds_count`
  * NOT work
    * Reason:🧠duplicate series | right hand-side🧠

* `prometheus_http_requests_total + on(handler, instance, job) prometheus_http_request_duration_seconds_count`
  * NOT work
    * Reason:🧠MANY left hand side's series match -> 1 right hand side's series🧠
    * Solution: `prometheus_http_requests_total + on(handler, instance, job) group_left prometheus_http_request_duration_seconds_count`
### `ignoring`
* `prometheus_http_requests_total + ignoring(code) prometheus_http_request_duration_seconds_count`
  * NOT work
    * Reason:🧠MANY left hand side's series match -> 1 right hand side's series🧠
    * Solution: `prometheus_http_requests_total + ignoring(code) group_left prometheus_http_request_duration_seconds_count`

## Types of matching
### 1to1 vector matches
#### `vector1 <operator> vector2`
##### 1! sample & labels match EXACTLY 
* `prometheus_tsdb_head_series == prometheus_tsdb_head_chunks`
  * `prometheus_tsdb_head_series{app="prometheus", instance="localhost:9090", job="prometheus"}`
  * `prometheus_tsdb_head_chunks{app="prometheus", instance="localhost:9090", job="prometheus"}`
##### SEVERAL samples by labels match EXACTLY
* `docker compose up -d`
* `up + prometheus_ready`
  * `up{instance="localhost:9090", job="prometheus22"}` & `up{instance="localhost:9090", job="prometheus"}`
  * `prometheus_ready{instance="localhost:9090", job="prometheus22"}` & `prometheus_ready{instance="localhost:9090", job="prometheus"}`
##### `<vector expr> <bin-op> ignoring(<label list>) <vector expr>`
* `prometheus_build_info + prometheus_ready`
  * Problems: "Empty query result This query returned no data"
    * `prometheus_build_info{branch, goarch, goos, goversion, instance, job, revision, tags, version}`
    * `prometheus_ready{instance, job}`
    * Solution: 💡`prometheus_build_info + ignoring(branch, goarch, goos, goversion, revision, tags, version) prometheus_ready`💡
##### `<vector expr> <bin-op> on(<label list>) <vector expr>`
* `prometheus_build_info + prometheus_ready`
  * Problems: "Empty query result This query returned no data"
    * `prometheus_build_info{branch, goarch, goos, goversion, instance, job, revision, tags, version}`
    * `prometheus_ready{instance, job}`
    * Solution: 💡`prometheus_build_info + on(instance, job) prometheus_ready`💡

### Manyto1 & 1toMany vector matches
#### `<vector expr> <bin-op> ignoring(<label list>) group_left(<label list>) <vector expr>`
* `prometheus_http_requests_total + ignoring(code) group_left() prometheus_http_request_duration_seconds_count`
  * `prometheus_http_requests_total{app, code, handler, instance, job}`
  * `prometheus_http_request_duration_seconds_count{app, handler, instance, job}`
* `prometheus_tsdb_head_samples_appended_total + ignoring(type) group_left() prometheus_tsdb_head_series`
  * `prometheus_tsdb_head_samples_appended_total{instance, job, type}`
  * `prometheus_tsdb_head_series{instance, job}`
* TODO: with group_left(<label list>)
#### `<vector expr> <bin-op> ignoring(<label list>) group_right(<label list>) <vector expr>`
* `prometheus_http_request_duration_seconds_count + ignoring(code) group_right() prometheus_http_requests_total`
* TODO: with group_right(<label list>)
#### `<vector expr> <bin-op> on(<label list>) group_left(<label list>) <vector expr>`
* `prometheus_tsdb_head_samples_appended_total + on(instance, job) group_left() prometheus_tsdb_head_series`
* TODO: with group_left(<label list>)
#### `<vector expr> <bin-op> on(<label list>) group_right(<label list>) <vector expr>`
* `prometheus_http_request_duration_seconds_count + on(app, handler, instance, job) group_right() prometheus_http_requests_total`
* TODO: with group_right(<label list>)

# Binary operator precedence
* TODO: