---
title: Querying basics
nav_title: Basics
sort_rank: 1
---

* Prometheus Query Language (PromQL)
  * == functional query language /
    * Reason of functional:🧠
      * aggregation
      * pure 
      * immutable
      * higher-order functions
      * declarative
        * == what you want != how to do🧠
    * provided 
      * -- by -- Prometheus
    * lets the user 
      * about time series data | real time,
        * select
        * aggregate 
    * 👀[types -- based on -- execution time](#expression-queries)👀
    * 💡`{__name__=~".+"}`💡
      * 's return
        * ALL supported metrics
  * ['s supported expressionS](#promqls-supported-expressions)
  * ALTERNATIVE
    * [HTTP API](api.md)

## Expression language returned data types

* Prometheus's language's expression OR sub-expression
  * 's result's ALLOWED types
    * **Instant vector**
      * == time serieS / 
        * 👀1! sample / EACH time series👀
        * ALL share the SAME timestamp
          * -> NOT displayed | Prometheus UI
      ```
      metric_name{labels} floatValue
      
      # if native histograms ingested | TSDB
      metric_name{labels} histogramOrFloatValue
      ```
    * **Range vector**
      * == time serieS /
        * has a range of data points | time / EACH time series
      ```
      metric_name{labels} floatValue @timestamp
      
      # if native histograms ingested | TSDB
      metric_name{labels} histogramOrFloatValue @timestamp
      ```
    * **Scalar**
      * == simple numeric floating point value
      ```
      {labels} floatValue
      ```
    * **String**
      * == simple string value
        * ⚠️CURRENTLY unused⚠️
          * Reason: 🧠's CURRENT design ONLY time series🧠

* see [native histograms](https://github.com/dancer1325/prometheus-website/blob/main/docs/specs/native_histograms.md)

## Expression queries
### Instant query
* == Prometheus UI's "Table" tab
* 👀evaluated | SOME point in time👀
* ALLOWED results
  * instant vector
  * scalar
  * string
* ❌NOT ALLOWED results❌
  * range vector
    * Reason:🧠| evaluate | specific time, IMPOSSIBLE to get range vector🧠

* | [API level](api.md#instant-queries)

### Range query
* == instant query / run MULTIPLE times | 
  * DIFFERENT timestamps
  * equally-spaced steps
* == Prometheus UI's "Graph" tab
* ALLOWED results
  * scalar
  * instant vector
* ❌NOT ALLOWED results❌
  * range vector
    * Reason:🧠| evaluate | specific time, IMPOSSIBLE to get range vector🧠
  * string 

* | [API level](api.md#range-queries)

## PromQL's supported expressions

### Literals

#### String literals

* String literals
  * syntax
    * 'stringValue'
    * "stringValue"
    * `stringValue`
  * 's escaping rules 
    * == [Go's escaping rules](https://golang.org/ref/spec#String_literals)
    * ALLOWED
      * |
        * ''
          * '\allowedEscapingRule'
        * ""
          * "\allowedEscapingRule"
      * escaping rules
        * `a`, `b`, `f`, `n`, `r`, `t`, `v` or `\`
        * notations
          * characters one (== BEFORE)
          * octal (`\nnn`)
          * hexadecimal (`\xnn`, `\unnnn` and `\Unnnnnnnn`)
    * -- via --
      * Prometheus UI
        * NOT return escaping
          * Reason:🧠ignore it🧠
      * API

#### Float literals and time durations
##### float literals 
* ways to write scalar float values
  * literal integer OR
  * literal floating-point numbers

    ```text
    [-+]?(
          [0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?
        | 0[xX][0-9a-fA-F]+
        | [nN][aA][nN]
        | [iI][nN][fF]
    )
    ```

* | decimal OR hexadecimal digits,
  * recommendations
    * if number is big -> use underscores (`_`)
      * Reason:🧠improve readability🧠

* uses
  * math operations
  * compare & filter

##### time durations
* `integerNumber` + `durationTimeUnit`
  * 👀syntax👀
  * if you
    * do NOT specify `durationTimeUnit` -> `s`
    * specify NOT integers -> NOT valid❌
  * 💡they can be concatenated💡/
    * order units: longest -- to -- shortest
      * ❌OTHERWISE, NOT valid❌
  * ALLOWED time units
    * `ms`
    * `s`
    * `m`
    * `h`
    * `d`
      * == days
    * `w`
      * == weeks
    * `y`
      * == years

* uses
  * range vectors
  * API parameters
  * offset modifiers

### Time series selectors

* uses
  * data / PromQL must fetch

#### Instant vector selectors

* allow
  * selecting a set of time serieS / 1! sample value / EACH time series | given timestamp
    * given
      * 👀by default, CURRENT👀
    * if you want to override the timestamp | select -> use [`@` modifier](#-modifier)
    * if time series' recent sample < time series' sample [lookback period](#staleness) ago -> time series returned

* ways
  * `metricName`
    * == `{__name__=metricName}`
    * keywords / NOT ALLOWED
      * `bool`
      * `on`
        * workaround -- `{__name__="on"}` -- 
      * `ignoring`
      * `group_left`
      * `group_right` 
  * `metricName{label1="value1",label2="value2",...}`
    * ways to match label vs value
      * operators
        * `=`
          * EXACTLY equal
        * `!=`
          * NOT equal
        * `=~`
          * 💡regex-match💡
          * -- based on -- [RE2 syntax](https://github.com/google/re2/wiki/Syntax)
          * FULLY anchored
            * | 
              * beginning, `^`
              * end, `$`
            * _Example:_ `env=~"foo"` -> `env=~"^foo$"` 
        * `!~`
          * NOT regex-match
      * if `label1=""` (== empty label value) -> select ALL time series / NOT have the specific label set
      * MULTIPLE matchers | SAME label name
        * ALL must match
  * requirements
    * specify `metricName` OR ( label matcher / NOT EMPTY string value)
      * Reason:🧠OTHERWISE, returns ALL metrics🧠

#### Range Vector Selectors

* Range vector selectors
  * 's work vs like instant vector selectors' work
    * SAME
      * EXCEPT, range of samples 👀(currentInstant - timeSpecified, currentInstant] 👀
        * LEFT is excluded
  * ways
    * `metricName[floatLiteral]`
    * `metricName{label1="value1",label2="value2",...}[floatLiteral]`

#### Offset modifier

* `offset` modifier
  * syntax
    * `instantVectorSelector offset floatLiteralDuration`
      * ❌️NOT valid❌
        * Reason:🧠| instant queries, ALWAYS return CURRENT or GIVEN timestamp🧠
    * `rangeVectorSelector offset floatLiteralDuration`
      * ❌if `offset` NOT IMMEDIATELY AFTER selector -> NOT valid❌
  * allows
    * changing the time offset (👀past or future👀) | range vectors
  * uses
    * ⚠️ONLY | range queries⚠️

#### @ modifier

* `@` modifier
  * syntax
    * `instantVectorSelector @ timestampAsFloatLiteral`
      * ❌️NOT valid❌
        * Reason:🧠| instant queries, ALWAYS return CURRENT or GIVEN timestamp🧠
    * `rangeVectorSelector @ timestampAsFloatLiteral`
      * ❌if `@` NOT IMMEDIATELY AFTER selector -> NOT valid❌
  * allows
    * changing the evaluation time | range vectors
  * uses
    * ⚠️ONLY | range queries⚠️

#### @ modifier + offset modifier OR offset modifier + @ modifier 
* `...` + (`offset timeDuration @ timeStamp` OR `@ timeStamp offset timeDuration`)
  * `offset` modifier is applied -- relative to the -- `@`modifier
  * uses 
    * ⚠️ONLY | range queries⚠️
      * ❌NOT valid | instant selectors❌

#### `@ start()` & `@ end()`

* allows
  * getting range query's start & end
* uses
  * range query

### Subquery

* Subquery
  * `<instant_query> '[' <range> ':' [<resolution>] ']' [ @ <float_literal> ] [ offset <float_literal> ]`
    * syntax
    * `<range>`
      * time durations
    * `<resolution>`
      * time durations
      * OPTIONAL
      * by default, `global.evaluation_interval`
  * allows
    * 👀run an instant query / given range & resolution👀
      * == 💡returns a range vector💡 

### Operators

* [expression language operators](operators.md)

### Functions

* [expression language functions](functions.md)

### Comments

```
# add a commentary
someQuery
```

## Gotchas

### Staleness

The timestamps at which to sample data, during a query, are selected
independently of the actual present time series data. This is mainly to support
cases like aggregation (`sum`, `avg`, and so on), where multiple aggregated
time series do not precisely align in time. Because of their independence,
Prometheus needs to assign a value at those timestamps for each relevant time
series. It does so by taking the newest sample that is less than the lookback period ago.
The lookback period is 5 minutes by default, but can be
[set with the `--query.lookback-delta` flag](../command-line/prometheus.md)

If a target scrape or rule evaluation no longer returns a sample for a time
series that was previously present, this time series will be marked as stale.
If a target is removed, the previously retrieved time series will be marked as
stale soon after removal.

If a query is evaluated at a sampling timestamp after a time series is marked
as stale, then no value is returned for that time series. If new samples are
subsequently ingested for that time series, they will be returned as expected.

A time series will go stale when it is no longer exported, or the target no
longer exists. Such time series will disappear from graphs
at the times of their latest collected sample, and they will not be returned
in queries after they are marked stale.

Some exporters, which put their own timestamps on samples, get a different behaviour:
series that stop being exported take the last value for (by default) 5 minutes before
disappearing. The `track_timestamps_staleness` setting can change this.

### Avoiding slow queries and overloads

If a query needs to operate on a substantial amount of data, graphing it might
time out or overload the server or browser. Thus, when constructing queries
over unknown data, always start building the query in the tabular view of
Prometheus's expression browser until the result set seems reasonable
(hundreds, not thousands, of time series at most).  Only when you have filtered
or aggregated your data sufficiently, switch to graph mode. If the expression
still takes too long to graph ad-hoc, pre-record it via a [recording
rule](../configuration/recording_rules.md#recording-rules).

This is especially relevant for Prometheus's query language, where a bare
metric name selector like `api_http_requests_total` could expand to thousands
of time series with different labels. Also, keep in mind that expressions that
aggregate over many time series will generate load on the server even if the
output is only a small number of time series. This is similar to how it would
be slow to sum all values of a column in a relational database, even if the
output value is only a single number.
