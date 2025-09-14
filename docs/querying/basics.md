---
title: Querying basics
nav_title: Basics
sort_rank: 1
---

* Prometheus Query Language (PromQL)
  * == functional query language /
    * provided 
      * -- by -- Prometheus
    * lets the user 
      * about time series data | real time,
        * select
        * aggregate 
    * 👀types -- based on -- execution time👀
      * [instant query](api.md#instant-queries)
        * == Prometheus UI's "Table" tab
        * evaluated | SOME point in time
        * supported types
          * ANY data type | root of the expression
      * [range query](api.md#range-queries) / equally-spaced steps
        * == instant query / run MULTIPLE times | DIFFERENT timestamps
        * == Prometheus UI's "Graph" tab 
        * supported types
          * scalar
          * instant vector
    * 👀functional ==👀
      * compose functions
      * input data do NOT change
      * pure functions
        * == SAME inputs -> SAME output
      * declarative expressions
        * != define required steps -- to -- calculate
    * 💡`{__name__=~".+"}`💡
      * 's return
        * ALL supported metrics
  * ALTERNATIVE
    * [HTTP API](api.md)

## Expression language data types

* Prometheus's expression language's expression OR sub-expression
  * 's result's ALLOWED types
    * **Instant vector**
      * == time series / 
        * has 1! sample / EACH time series
        * ALL share the SAME timestamp
          * -> NOT displayed | Prometheus UI
      ```
      metric_name{labels} value
      ```
    * **Range vector**
      * == time series /
        * has a range of data points | time / EACH time series
      ```
      metric_name{labels} value @timestamp
      ```
    * **Scalar**
      * == simple numeric floating point value
      ```
      {labels} value
      ```
    * **String**
      * == simple string value
        * ⚠️CURRENTLY unused⚠️

_Notes about the experimental native histograms:_

* Ingesting native histograms has to be enabled via a [feature
  flag](../feature_flags.md#native-histograms).
* Once native histograms have been ingested into the TSDB (and even after
  disabling the feature flag again), both instant vectors and range vectors may
  now contain samples that aren't simple floating point numbers (float samples)
  but complete histograms (histogram samples). A vector may contain a mix of
  float samples and histogram samples. Note that the term “histogram sample” in
  the PromQL documentation always refers to a native histogram. Classic
  histograms are broken up into a number of series of float samples. From the
  perspective of PromQL, there are no “classic histogram samples”.
* Like float samples, histogram samples can have a counter or a gauge “flavor”,
  marking them as counter histograms or gauge histograms, respectively. In
  contrast to float samples, histogram samples “know” their flavor, allowing
  reliable warnings about mismatched operations (e.g. applying the `rate`
  function to a range vector of gauge histograms).
* Native histograms can have different bucket layouts, but they are generally
  convertible to compatible versions to apply binary and aggregation operations
  to them. This is not true for all bucketing schemas. If incompatible
  histograms are encountered in an operation, the corresponding output vector
  element is removed from the result, flagged with a warn-level annotation.
  More details can be found in the [native histogram
  specification](https://prometheus.io/docs/specs/native_histograms/#compatibility-between-histograms).

## Literals

### String literals

String literals are designated by single quotes, double quotes or backticks.

PromQL follows the same [escaping rules as
Go](https://golang.org/ref/spec#String_literals). For string literals in single or double quotes, a
backslash begins an escape sequence, which may be followed by `a`, `b`, `f`,
`n`, `r`, `t`, `v` or `\`.  Specific characters can be provided using octal
(`\nnn`) or hexadecimal (`\xnn`, `\unnnn` and `\Unnnnnnnn`) notations.

Conversely, escape characters are not parsed in string literals designated by backticks. It is important to note that, unlike Go, Prometheus does not discard newlines inside backticks.

Example:

    "this is a string"
    'these are unescaped: \n \\ \t'
    `these are not unescaped: \n ' " \t`

### Float literals and time durations

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
    * use underscores (`_`)
      * Reason:🧠improve readability🧠

* durations
  * uses
    * `integerNumber` + `durationTimeUnit`
      * if you
        * do NOT specify `durationTimeUnit` -> `s`
        * specify NOT integers -> NOT valid❌
      * 💡they can be concatenated💡/
        * order units: longest -- to -- shortest
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

## Time series selectors

* == basic building-blocks /
  * uses
    * what data / PromQL must fetch

### Instant vector selectors

Instant vector selectors allow the selection of a set of time series and a
single sample value for each at a given timestamp (point in time).  In the simplest
form, only a metric name is specified, which results in an instant vector
containing elements for all time series that have this metric name.

The value returned will be that of the most recent sample at or before the
query's evaluation timestamp (in the case of an
[instant query](api.md#instant-queries))
or the current step within the query (in the case of a
[range query](api.md#range-queries)).
The [`@` modifier](#modifier) allows overriding the timestamp relative to which
the selection takes place. Time series are only returned if their most recent sample is less than the [lookback period](#staleness) ago.

This example selects all time series that have the `http_requests_total` metric
name, returning the most recent sample for each:

    http_requests_total

It is possible to filter these time series further by appending a comma-separated list of label
matchers in curly braces (`{}`).

This example selects only those time series with the `http_requests_total`
metric name that also have the `job` label set to `prometheus` and their
`group` label set to `canary`:

    http_requests_total{job="prometheus",group="canary"}

It is also possible to negatively match a label value, or to match label values
against regular expressions. The following label matching operators exist:

* `=`: Select labels that are exactly equal to the provided string.
* `!=`: Select labels that are not equal to the provided string.
* `=~`: Select labels that regex-match the provided string.
* `!~`: Select labels that do not regex-match the provided string.

[Regex](#regular-expressions) matches are fully anchored. A match of `env=~"foo"` is treated as `env=~"^foo$"`.

For example, this selects all `http_requests_total` time series for `staging`,
`testing`, and `development` environments and HTTP methods other than `GET`.

    http_requests_total{environment=~"staging|testing|development",method!="GET"}

Label matchers that match empty label values also select all time series that
do not have the specific label set at all. It is possible to have multiple matchers for the same label name.

For example, given the dataset:

    http_requests_total
    http_requests_total{replica="rep-a"}
    http_requests_total{replica="rep-b"}
    http_requests_total{environment="development"}

The query `http_requests_total{environment=""}` would match and return:

    http_requests_total
    http_requests_total{replica="rep-a"}
    http_requests_total{replica="rep-b"}

and would exclude:

    http_requests_total{environment="development"}

Multiple matchers can be used for the same label name; they all must pass for a result to be returned.

The query:

    http_requests_total{replica!="rep-a",replica=~"rep.*"}

Would then match:

    http_requests_total{replica="rep-b"}

Vector selectors must either specify a name or at least one label matcher
that does not match the empty string. The following expression is illegal:

    {job=~".*"} # Bad!

In contrast, these expressions are valid as they both have a selector that does not
match empty label values.

    {job=~".+"}              # Good!
    {job=~".*",method="get"} # Good!

Label matchers can also be applied to metric names by matching against the internal
`__name__` label. For example, the expression `http_requests_total` is equivalent to
`{__name__="http_requests_total"}`. Matchers other than `=` (`!=`, `=~`, `!~`) may also be used.
The following expression selects all metrics that have a name starting with `job:`:

    {__name__=~"job:.*"}

The metric name must not be one of the keywords `bool`, `on`, `ignoring`, `group_left` and `group_right`. The following expression is illegal:

    on{} # Bad!

A workaround for this restriction is to use the `__name__` label:

    {__name__="on"} # Good!

### Range Vector Selectors

Range vector literals work like instant vector literals, except that they
select a range of samples back from the current instant. Syntactically, a
[float literal](#float-literals-and-time-durations) is appended in square
brackets (`[]`) at the end of a vector selector to specify for how many seconds
back in time values should be fetched for each resulting range vector element.
Commonly, the float literal uses the syntax with one or more time units, e.g.
`[5m]`. The range is a left-open and right-closed interval, i.e. samples with
timestamps coinciding with the left boundary of the range are excluded from the
selection, while samples coinciding with the right boundary of the range are
included in the selection.

In this example, we select all the values recorded less than 5m ago for all
time series that have the metric name `http_requests_total` and a `job` label
set to `prometheus`:

    http_requests_total{job="prometheus"}[5m]

### Offset modifier

The `offset` modifier allows changing the time offset for individual
instant and range vectors in a query.

For example, the following expression returns the value of
`http_requests_total` 5 minutes in the past relative to the current
query evaluation time:

    http_requests_total offset 5m

Note that the `offset` modifier always needs to follow the selector
immediately, i.e. the following would be correct:

    sum(http_requests_total{method="GET"} offset 5m) // GOOD.

While the following would be *incorrect*:

    sum(http_requests_total{method="GET"}) offset 5m // INVALID.

The same works for range vectors. This returns the 5-minute [rate](./functions.md#rate)
that `http_requests_total` had a week ago:

    rate(http_requests_total[5m] offset 1w)

When querying for samples in the past, a negative offset will enable temporal comparisons forward in time:

    rate(http_requests_total[5m] offset -1w)

Note that this allows a query to look ahead of its evaluation time.

### @ modifier

The `@` modifier allows changing the evaluation time for individual instant
and range vectors in a query. The time supplied to the `@` modifier
is a Unix timestamp and described with a float literal.

For example, the following expression returns the value of
`http_requests_total` at `2021-01-04T07:40:00+00:00`:

    http_requests_total @ 1609746000

Note that the `@` modifier always needs to follow the selector
immediately, i.e. the following would be correct:

    sum(http_requests_total{method="GET"} @ 1609746000) // GOOD.

While the following would be *incorrect*:

    sum(http_requests_total{method="GET"}) @ 1609746000 // INVALID.

The same works for range vectors. This returns the 5-minute rate that
`http_requests_total` had at `2021-01-04T07:40:00+00:00`:

    rate(http_requests_total[5m] @ 1609746000)

The `@` modifier supports all representations of numeric literals described above.
It works with the `offset` modifier where the offset is applied relative to the `@`
modifier time.  The results are the same irrespective of the order of the modifiers.

For example, these two queries will produce the same result:

    # offset after @
    http_requests_total @ 1609746000 offset 5m
    # offset before @
    http_requests_total offset 5m @ 1609746000

Additionally, `start()` and `end()` can also be used as values for the `@` modifier as special values.

For a range query, they resolve to the start and end of the range query respectively and remain the same for all steps.

For an instant query, `start()` and `end()` both resolve to the evaluation time.

    http_requests_total @ start()
    rate(http_requests_total[5m] @ end())

Note that the `@` modifier allows a query to look ahead of its evaluation time.

## Subquery

Subquery allows you to run an instant query for a given range and resolution. The result of a subquery is a range vector.

Syntax: `<instant_query> '[' <range> ':' [<resolution>] ']' [ @ <float_literal> ] [ offset <float_literal> ]`

* `<resolution>` is optional. Default is the global evaluation interval.

## Operators

Prometheus supports many binary and aggregation operators. These are described
in detail in the [expression language operators](operators.md) page.

## Functions

Prometheus supports several functions to operate on data. These are described
in detail in the [expression language functions](functions.md) page.

## Comments

PromQL supports line comments that start with `#`. Example:

        # This is a comment

## Regular expressions

All regular expressions in Prometheus use [RE2 syntax](https://github.com/google/re2/wiki/Syntax).

Regex matches are always fully anchored.

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
