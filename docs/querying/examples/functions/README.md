* `docker compose up -d`

# `abs(v instant-vector)`
* `abs(prometheus_ready - 2*up)`
  * vs `prometheus_ready - 2*up`
## NOT valid | scalar
* `abs(2-3)`
## `v`'s ALL float samples are converted -- to -- their absolute value
* `abs(delta(go_memstats_heap_inuse_bytes[5m]))` vs `delta(go_memstats_heap_inuse_bytes[5m])` 
## use case | subtract metrics
* `abs(prometheus_ready - 2*up)` vs `prometheus_ready - 2*up`

# `absent(v instant-vector)`

# `<aggregation>_over_time()`
## `avg_over_time(range-vector)`
### float samples
* `avg_over_time(process_cpu_seconds_total[1h])`
  * vs `process_cpu_seconds_total` | graph
### histogram samples
* TODO:
## `min_over_time(range-vector)`
### float samples
* `min_over_time(process_cpu_seconds_total[1h])`
  * vs `process_cpu_seconds_total` | graph
### histogram samples, NOT valid
* TODO:
## `max_over_time(range-vector)`
### float samples
* `max_over_time(process_cpu_seconds_total[1h])`
  * vs `process_cpu_seconds_total` | graph
### histogram samples, NOT valid
* TODO:
## `sum_over_time(range-vector)`
### float samples
* `sum_over_time(process_cpu_seconds_total[1h])`
  * value comes from
    * 1 hora / (15 scrapes/1second) == 240 data points
  * vs `process_cpu_seconds_total` | graph
### histogram samples
* TODO:
## `count_over_time(range-vector)`
* `count_over_time(process_cpu_seconds_total[1h])`
## `quantile_over_time(scalar, range-vector)`
* `quantile_over_time(0.3, process_open_fds[1h])`
  * < `quantile_over_time(0.9, process_open_fds[1h])`
    * Reason:🧠90% of values are < this value🧠
### NOT uses | counter
* `quantile_over_time(0.9, process_cpu_seconds_total[1h])`
  * check `process_cpu_seconds_total` | graph == cumulative
## TODO:
## `last_over_time(range-vector)`
* `last_over_time(process_open_fds[1h])`
  * == `process_open_fds[1h]` | end of the interval
## `present_over_time(range-vector)`
### ALTHOUGH the sample's value == 0 -> return 1
* `present_over_time(prometheus_api_notification_updates_sent_total[10m])`
  * see `prometheus_api_notification_updates_sent_total` | graph | LAST 10m
### if there are NO series | specified interval -> returns 0
* `docker compose stop spring-app`
* hold on | 1m
* `present_over_time(jvm_buffer_memory_used_bytes[1m])`
  * return 0
  * see `jvm_buffer_memory_used_bytes` | graph | LAST 10m

# `day_of_week(v=vector(time()) instant-vector)`
* `day_of_week()`
## if there are histogram samples -> ignored
* TODO:
## uses
### temporal filters
* `day_of_week() >= 1 and day_of_week() <= 5`
  * == working days

# `hour(v=vector(time()) instant-vector)`
* `hour()`
  * CURRENT hour | UTC
    * [UTC vs CEST](https://www.utctime.net/utc-to-cest-converter)
## 's input are histogram samples -> ignored
* TODO:
## uses
### CURRENT timestamp
* `hour()`
### timestamp's hour
* `hour(timestamp(prometheus_http_requests_total))`
### temporal filters
* `prometheus_http_requests_total and (hour() >= 9 and hour() <= 17)`
  * Problems:
    * Problem1: "Empty query result"
      * Solution: TODO:

# `increase(v range-vector)`
* `increase(prometheus_http_requests_total{handler="/metrics"}[10m])`
## if there are NO scrapes | end of time range -> extrapolates | ends of the time range
* `increase(prometheus_http_requests_total{handler="/metrics"}[10m])` vs `prometheus_http_requests_total{handler="/metrics"}[10m]`
## if there is a break in monotonicity -> AUTOMATICALLY adjusted for
* `rate(jvm_compilation_time_ms_total[3m])`
* `docker compose restart spring-app`
  * break in monotonicity
* `rate(jvm_compilation_time_ms_total[3m])`
## uses |
### NO counters
* TODO:
### counters
#### float samples
* TODO:
#### histograms
##### calculate a new histogram / EACH component (`_sum`, `_count`, `_bucket`) == increase | [first native histogram, last native histogram]
* TODO:
##### if there are `v`'s elements / have float samples + native histograms | range -> omitted | result vector
* TODO:
## == 👀rate(v range-vector) * timeRangeInSeconds👀
* `increase(prometheus_http_requests_total{handler="/metrics"}[1h])` == `rate(prometheus_http_requests_total{handler="/metrics"}[1h])*3600`

# `irate(v range-vector)`
* `irate(prometheus_http_requests_total{handler="/metrics"}[5m])`
## -- based on -- last 2 data points
* refresh SEVERAL times http://localhost:9090/metrics
* `irate(prometheus_http_requests_total{handler="/metrics"}[5m])`
  * AFTER 2 scrapes WITHOUT hitting, come back to raw rate
    * != `rate`
### if samples are float & histogram -> 1 of those is omitted | result vector
* TODO:
## if there is a break in monotonicity -> AUTOMATICALLY adjusted for
* `rate(jvm_compilation_time_ms_total[3m])`
* `docker compose restart spring-app`
    * break in monotonicity
* `rate(jvm_compilation_time_ms_total[3m])`
    * adjusted / notice a break
## \+
### aggregation operator
* `sum(irate(prometheus_http_requests_total[2m])) by (job)`
* `irate(sum(prometheus_http_requests_total)[2m])`
  * ❌NOT valid❌
    * Reason: 🧠`sum(prometheus_http_requests_total)` != vector selector🧠
### function aggregating over time
* `max_over_time(irate(prometheus_http_requests_total[2m])[20m:])`
* `irate(max_over_time(prometheus_http_requests_total[20m:])[2m])`
  * ❌NOT valid❌
    * Reason: 🧠`sum(prometheus_http_requests_total)` != vector selector🧠

# `rate(v range-vector)`
* `rate(prometheus_http_requests_total{handler="/metrics"}[5m])`
  * refresh SEVERAL times http://localhost:9090/metrics
## if there is a break in monotonicity -> AUTOMATICALLY adjusted for
* `rate(jvm_compilation_time_ms_total[3m])`
* `docker compose restart spring-app`
  * break in monotonicity
* `rate(jvm_compilation_time_ms_total[3m])`
  * adjusted / notice a break
## if there are NO scrapes | end of time range -> extrapolates | ends of the time range
* `rate(prometheus_http_requests_total{handler="/api/v1/notifications/live"}[5m])` vs `prometheus_http_requests_total{handler="/api/v1/notifications/live"}[5m]`
## uses | 
### NO counters
* `rate(jvm_buffer_count_buffers[1m])`
  * you get an info message "PromQL info: metric might not be a counter, name does not end in _total/_sum/_count/_bucket: "jvm_buffer_count_buffers" (1:6)"
### counters 
#### float samples
* `rate(jvm_compilation_time_ms_total[3m])`
#### histograms
##### calculate a new histogram / EACH component == rate of increase | [first native histogram, last native histogram]
* TODO:
#### if there are `v`'s elements / have float samples + native histograms | range -> omitted | result vector
* TODO:
## \+
### aggregation operator
* `sum(rate(prometheus_http_requests_total[2m])) by (job)`
* `rate(sum(prometheus_http_requests_total)[2m])`
  * ❌NOT valid❌
    * Reason: 🧠`sum(prometheus_http_requests_total)` != vector selector🧠
### function aggregating over time
* `max_over_time(rate(prometheus_http_requests_total[2m])[20m:])`
* `rate(max_over_time(prometheus_http_requests_total[20m:])[2m])`
  * ❌NOT valid❌
    * Reason: 🧠`sum(prometheus_http_requests_total)` != vector selector🧠


# `round(v instant-vector, [to_nearest=1 scalar])`
## OPTIONAL
### by default 1 == unit
* `process_cpu_seconds_total` vs `round(process_cpu_seconds_total)`
### if you specify
* `process_cpu_seconds_total` vs `round(process_cpu_seconds_total, 0.1)`
  * `0.1` == round to decima
## if there are ties -> round up
* `process_cpu_seconds_total` vs `round(process_cpu_seconds_total, 0.1)`
  * WAIT for `process_cpu_seconds_total` = *.5

# `time()`
* `time()`
  * ONLY this -> CURRENT timestamp
## uses
### process uptime
* `time() - process_start_time_seconds`
### calculations -- based on -- time
* `time() - timestamp(prometheus_http_requests_total)` & `time() - timestamp(go_gc_duration_seconds)`
  * == time BETWEEN LAST scrape
    * SAME | ALL SAME target's metrics to scrap

# `timestamp(v instant-vector)`
## vector's sample's timestamp / specified -- as -- number of seconds since January 1, 1970 UTC
* `timestamp(prometheus_http_requests_total)`
  * == CURRENTLY
## uses
### calculations -- based on -- time
* `time() - timestamp(prometheus_http_requests_total)` & `time() - timestamp(go_gc_duration_seconds)`
    * == time BETWEEN LAST scrape
