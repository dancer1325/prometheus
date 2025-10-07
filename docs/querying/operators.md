---
title: Operators
sort_rank: 2
---

# PrompQL's supported operators
## Unary operator

* `-`
  * unary minus
  * 👀ONLY PromQL's unary operator👀
  * uses |
    * scalar
      * 's return
        * scalar / inverted sign 
    * instant vector
      * 's return
        * instant vector / inverted sign / EACH element
          * if it's a histogram sample -> invert
            * ALL bucket populations' sign
            * count
            * sum of observations

## Binary operators

### Arithmetic binary operators

* are
  * `+`
    * (addition)
  * `-`
    * (subtraction)
  * `*`
    * (multiplication)
  * `/`
    * (division)
  * `%`
    * (modulo)
  * `^`
    * (power/exponentiation)

* ALLOWED |
  * scalar -- & -- scalar
  * vector -- & -- scalar
    * == 👀vector's EACH sample + arithmetic binary operator + scalar👀
      * 's return
        * if vector's sample 
          * == float -> 's return == vector
          * == ⚠️native histogram &
            * `*` ⚠️
              * -> ALL bucket populations and the count and the sum of observations are multiplied by the scalar
              * & scalar is negative -> returns a gauge histogram
            * `/`
              * -> `histogram / scalar`
                * == histogram | left hand side & scalar | right hand side
                  * EACH bucket's value / scalar
                  * count / scalar
                  * sum / scalar
                * & scalar=0
                  * NO regular buckets
                  * return count & sum == `+Inf`, `-Inf`, or `NaN`
                * & scalar<0
                  * return == gauge histogram
  * vector -- & -- vector
    * == 👀vector's EACH entry + arithmetic binary operator + vector's EACH entry👀
      * -- via -- [vector matching](#vector-matching)
    * if there is a matching label / NOT match value -> NOT include | result
      ```
      http_requests_total{instance="server1", job="web"} = 100
      http_requests_total{instance="server2", job="web"} = 200
      http_requests_total{instance="server3", job="api"} = 150

      http_request_duration_count{instance="server1", job="web"} = 80
      http_request_duration_count{instance="server2", job="web"} = 120

      http_requests_total + http_request_duration_count
      # {instance="server1", job="web"} = 180  # 100 + 80 
      # {instance="server2", job="web"} = 320  # 200 + 120 
      # server3/api NO included
      ```
    * if BOTH are histograms -> ONLY valid operations: `+` and `-` 
      * recommendations
        * ONLY use | gauge histograms
          * ALTHOUGH you can use ALSO | counter histogram 

* rules
  * follow [IEEE 754 floating point arithmetic](https://en.wikipedia.org/wiki/IEEE_754)

* metric name
  * ⚠️dropped⚠️
    * EVEN if you add `on(__name__)`
    * [issue](https://github.com/prometheus/prometheus/issues/16631)

### Trigonometric binary operators

* are
  * `atan2`
    * == arc tangent
    * -- based on -- https://pkg.go.dev/math#Atan2
    * unit: radians

* allows
  * executing trigonometric functions | 2 vectors
    * ⚠️-- via -- [vector matching](#vector-matching)⚠️
      * == required to vector match
    * NOT available -- via -- normal functions
    * if they are histogram samples -> remove output vector's corresponding vector elements / flag by an info-level annotation

### Comparison binary operators

* are
  * `==`
    * equal
  * `!=` 
    * not-equal
  * `>` 
    * greater-than
  * `<` 
    * less-than
  * `>=` 
    * greater-or-equal
  * `<=` 
    * less-or-equal

* ALLOWED |
  * scalar/scalar
    * ⚠️requirements⚠️
      * `bool`
  * vector/scalar
    * if vector's sample == histogram -> corresponding result vector's element is removed
    * if vector elements comparison is false -> dropped from the result vector
  * vector/vector
    * if vector elements / expression is NOT true OR NOT find a match -> dropped from the result

* `bool`
  * `leftSide <binaryOperator> bool rightSide`
  * allows
    * 👀return `0` OR `1`👀
      * != filtering 
  * if vector | SOME side -> metric name is dropped
    * OTHERWISE, add left side's metric name
  * if vectorS comparison / match & expression false
    * -> return "Empty query result"
    * & use `bool` -> return `1` 

* match 
  * float sample & histogram sample
    * invalid
      * == removed from the result vector
  * BETWEEN 2 histogram samples
    * ONLY valid
      * `==`
      * `!=`

* metric name
  * if `on` is used -> it's dropped
  * if `group_right` is used -> right side's metric name 

### Logical/set binary operators

* uses
  * 👀BETWEEN instant vectors👀
    * valid |
      * float samples
      * histogram samples

* built-in
  * `and`
    * intersection
      * `vector1`'s elements == `vector2`'s elements /
        * EXACTLY match label sets
    * `vector1 and vector2`
    * 's return
      * == vector /  
        * 's metric name == left side's metric name
        * 's values == left side's values
  * `or`
    * union
    * 's return
      * == vector / contains
        * ALL `vector1`'s original elements + ALL `vector2`'s elements / NOT have `vector1`'s matching label sets 
  * `unless`
    * complement
    * 's return
      * == vector / contains
        * `vector1`'s elements / NO `vector2`'s elements EXACTLY matching label sets 

* by default,
  * match with ALL possible entries | right vector

## Aggregation operators

* built-in aggregation operators
  * `sum(v)`
    * sum over dimensions
  * `avg(v)`
    * arithmetic average over dimensions
  * `min(v)` & `max(v)` 
    * select minimum OR maximum over dimensions
  * `bottomk(k, v)` & `topk(k, v)` 
    * 's input
      * `k`
        * integer
      * `v`
        * metric
    * 's return
      * smallest OR largest `k` elements by sample value
  * `limitk(k, v)` 
    * **experimental**
    * requirements
      * `--enable-feature=promql-experimental-functions`
    * sample `k` elements  
  * `limit_ratio(r, v)` 
    * **experimental**
    * requirements
      * `--enable-feature=promql-experimental-functions`
    * sample a pseudo-random ratio `r` of elements  
  * `group(v)` 
    * group ALL values
      * == 1
  * `count(v)` 
    * count `v`'s number of elements
  * `count_values(l, v)` 
    * count number of `v`'s elements / filter by `l`
  * `stddev(v)` 
    * population standard deviation over dimensions
  * `stdvar(v)` 
    * population standard variance over dimensions
  * `quantile(φ, v)` 
    * calculate φ-quantile (0 ≤ φ ≤ 1) over dimensions

* allows
  * aggregate 1! instant vector's elements
    * -> new vector OF fewer elements / aggregated values 
    * uses
      * aggregate over ALL label dimensions
      * preserve distinct dimensions -- by including -- `without` OR `by`

        ```
        # BEFORE the expression
        <aggr-op> [without|by (<label list>)] ([parameter,] <vector expression>)
        
        # AFTER the expression
        <aggr-op>([parameter,] <vector expression>) [without|by (<label list>)]
        ```
        * `without`
          * removes result vector's listed labels
        * `by`
          * specify result vector's listed labels
        * `(<label list>)`
          * == unquoted labelS / may include a trailing comma

### `sum(v)`
* `sum(v)`
  * sums up `v`'s sample values
    * == `+` binary operator
    * requirements
      * ALL `v`'s sample values MUST be
        * float samples OR
        * histogram samples
  * 's return
    * 1! vector

### `avg(v)`

* `avg(v)`
  * == `sum(v) / numberOfAggregatedSamples`
    * requirements
      * ALL `v`'s sample values MUST be
        * float samples OR
        * histogram samples

### `min(v)` & `max(v)`

* uses
  * ⚠️ONLY | float samples⚠️

* if ALL aggregated values are `NaN` -> returns `NaN`

### `topk` & `bottomk`

* `topk(k, v)` and `bottomk(k, v)`
  * 's return
    * vector / contains the original labels 

* `by` & `without`
  * `by`
    * `topk(k, v) by (label)` OR `bottomk(k, v) by (label)`
  * `without`
    * `topk(k, v) without (labelS)` OR `bottomk(k, v) without (labelS)`
  * allows
    * 💡bucket the `v`💡
      * `by (label)`
        * label -- by which -- bucket
      * `without (label)`
        * exclude labels -- by which -- bucket
  * ❌NO guarantee / buckets of series are returned | any particular order❌ 
    * == DIFFERENT order | SAME hit

* uses
  * ⚠️ONLY | float samples⚠️

* if there are `NaN` values -> the farthest from the top or bottom

### `limitk(k,v)` 

* 's input
  * `k`
    * integer
  * `v`
    * instant vector
* 's return
  * subset of `k` input samples / 
    * includes `v`'s original labels
    * selected -- via -- deterministic pseudo-random way

* ALLOWED |
  * float samples
  * histogram samples

### `limit_ratio(r, v)`

* 's input
  * `r`
    * ALLOWED values: [-1, +1]
    * absolute value of r == selection ratio
    * if r = -1 -> complementary
* 's return
  * subset `r`* 100% of `v` input samples /
    * includes `v`' original labels
    * selected -- via -- deterministic pseudo-random way

* ALLOWED |
  * float samples
  * histogram samples

### `group(v)`

* `group(v)`
  * 's return
    * 1 / EACH group / contains any value | that timestamp
  * `group(v) by(labelsToGroup)` OR `group(v) without(labelsByExclude)`

* ALLOWED values
  * float sample
  * histogram sample

### `count(v)`
* 's return
  * number of values | that timestamp OR
  * if NO values | that timestamp -> NO value
  
* ALLOWED values
  * float sample
  * histogram sample

### `count_values(l, v)` 
* 's input
  * `l`
    * `v`'s label / filter in
  * `v`
    * vector
* 's return
  * time series / EACH sample value
    * label's name == l

* ALLOWED values
  * float sample
  * histogram sample

### `stddev(v)`
* 's input
  * ⚠️ONLY float sample / follow [IEEE 754 floating point arithmetic](https://en.wikipedia.org/wiki/IEEE_754) ⚠️
    * if you pass histogram samples -> ignored
* 's return
  * the standard deviation of `v`

### `stdvar(v)`
* 's input
  * ⚠️ONLY float sample / follow [IEEE 754 floating point arithmetic](https://en.wikipedia.org/wiki/IEEE_754) ⚠️
    * if you pass histogram samples -> ignored
* 's return
  * standard variance of `v`

### `quantile(φ, v)`

* 's input
  * `φ`
    * phi-quantile 
  * `v`
    * ONLY | flot samples

* `NaN`
  * the smallest possible value

* _Example:_
  * `quantile(0.5, ...)` == median
  * `quantile(0.95, ...)` == 95th percentile
  * φ = `NaN` -> returns `NaN`
  * φ < 0 -> returns `-Inf`
  * φ > 1 -> returns `+Inf`

# Vector matching

* uses
  * operations BETWEEN vectors
* goal
  * 👀find a matching element | right-hand side vector / EACH entry | left-hand side👀

## Vector matching keywords

* allows
  * matching series / have DIFFERENT label sets

* built-in
  * `on`

    ```
    vector1 <operator> on(<label1>, <label2>, ...) vector2
    ```
    * `<labeli>`
      * 👀labels / used -- for -- matching👀

  * `ignoring`
    ```
    vector1 <operator> ignoring(<label1>, <label2>, ...) vector2
    ```
    * `<labeli>`
      * 👀labels / NOT used -- for -- matching👀

## Group modifiers

* enable [many-to-one/one-to-many vector matching](#many-to-one-and-one-to-many-vector-matches)

* built-in
  * `group_left`
  * `group_right`

* allows
  * | 1ToMany or ManyTo1,
    * 💡include "1"-side's labels💡

* uses
  * [comparison 1toMany](#comparison-binary-operators)
  * [arithmetic 1toMany](#arithmetic-binary-operators)

## Types of matching
### 1to1 vector matches

* goal
  * 👀finds 1! pair of entries / EACH side of the operation👀

* `vector1 <operator> vector2`
  * default case

* 💡if 2 entries have the exact SAME set of labels & corresponding values -> BOTH entries match💡 

* built-in keywords
  * `ignoring` keyword
    * allows
      * 👀| match 2 entries, ignore certain label👀
        * Reason: 🧠OTHERWISE, they do NOT match🧠
    ```
    <vector expr> <bin-op> ignoring(<label list>) <vector expr>
    ```
  * `on` keyword
    * allows
      * 👀| match 2 entries, specify the considered labels👀
    ```
    <vector expr> <bin-op> on(<label list>) <vector expr>
    ```

 ### Manyto1 & 1toMany vector matches

* ALTERNATIVE
  * `ignoring(<labels>)`

* uses
  * 👀EACH vector element | "1"-side can match -- with -- MULTIPLE elements | "many"-side👀

```
<vector expr> <bin-op> ignoring(<label list>) group_left(<label list>) <vector expr>
<vector expr> <bin-op> ignoring(<label list>) group_right(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) group_left(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) group_right(<label list>) <vector expr>
```

* `group_left` or `group_right`
  * 💡determines the vector / has the higher cardinality💡
    * if left hand side == MANY (== higher cardinality) -> use `group_left`
    * if right hand side == MANY (== higher cardinality) -> use `group_right`
  * `(<label list>)`
    * == "1"-side's additional labels / included | result metrics
    * OPTIONAL

* if you use `on(<label list>)` -> label can ONLY appear | `on`'s list OR `group_left` OR `group_right`'s list

# Binary operator precedence

* Prometheus' binary operators precedence / from highest -- to -- lowest
  1. `^`
  2. `*`, `/`, `%`, `atan2`
  3. `+`, `-`
  4. `==`, `!=`, `<=`, `<`, `>=`, `>`
  5. `and`, `unless`
  6. `or`

* if operators have SAME precedence -> left-associative
  * _Example:_ `2 * 3 % 2` == `(2 * 3) % 2`
  * EXCEPTION, 
    * `^` is right associative
      * _Example:_ `2 ^ 3 ^ 2` == `2 ^ (3 ^ 2)`
