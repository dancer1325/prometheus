# Usage

* TSDB
  * used by
    * OTHER applications
      * [Cortex](https://cortexmetrics.io/)
      * [Thanos](https://thanos.io/)
      * [Grafana Mimir](https://grafana.com/oss/mimir/)

* _Examples:_
  * [example_test.go](../example_test.go)
  * [db_test.go](../db_test.go)

## Instantiating a database

* [`func Open(dir string, l *slog.Logger, r prometheus.Registerer, opts *Options, stats *DBStats) (db *DB, err error) {}`](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb#Open) 
  * open a TSDB
  * 's input
    * `dir string`
      * ALLOWED ones
        * NEW OR
        * pre-existing
  * 's return
    * [`*tsdb.DB`](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb#DB)
      * == actual database

A `DB` has the following main components:

* Compactor: a [leveled compactor](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb#LeveledCompactor). Note: it is currently the only compactor implementation. It runs automatically.
* [`Head`](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb#DB.Head)
* [Blocks (persistent blocks)](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb#DB.Blocks)

The `Head` is responsible for a lot. Here are its main components:

* [WAL](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb/wal#WAL) (Write Ahead Log).
* [`stripeSeries`](https://github.com/prometheus/prometheus/blob/411021ada9ab41095923b8d2df9365b632fd40c3/tsdb/head.go#L1292):
  this holds all the active series by linking to [`memSeries`](https://github.com/prometheus/prometheus/blob/411021ada9ab41095923b8d2df9365b632fd40c3/tsdb/head.go#L1462)
  by an ID (aka "ref") and by labels hash.
* Postings list (reverse index): For any label-value pair, holds all the corresponding series refs. Used for queries.
* Tombstones.

## Adding data

Use [`db.Appender()`](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb#DB.Appender) to obtain an "appender".
The [golang docs](https://pkg.go.dev/github.com/prometheus/prometheus/storage#Appender) speak mostly for themselves.

Remember:

* Use `Commit()` to add the samples to the DB and update the WAL.
* Create a new appender each time you commit.
* Appenders are not concurrency safe, but scrapes run concurrently and as such, leverage multiple appenders concurrently.
  This reduces contention, although Commit() contend the same critical section (writing to the WAL is serialized), and may
  inflate append tail latency if multiple appenders try to commit at the same time.

Append may reject data due to these conditions:

1) `timestamp < minValidTime` where `minValidTime` is the highest of:
  * the maxTime of the last block (i.e. the last truncation time of Head) - updated via [`Head.Truncate()`](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb#Head.Truncate) and [`DB.compactHead()`](https://github.com/prometheus/prometheus/blob/411021ada9ab41095923b8d2df9365b632fd40c3/tsdb/db.go#L968)
  * `tsdb.min-block-duration/2` older than the max time in the Head block. Note that while technically `storage.tsdb.min-block-duration` is configurable, it's a hidden option and changing it is discouraged.  So We can assume this value to be 2h.

  Breaching this condition results in "out of bounds" errors.  
  The first condition assures the block that will be generated doesn't overlap with the previous one (which simplifies querying)  
  The second condition assures the sample won't go into the so called "compaction window", that is the section of the data that might be in process of being saved into a persistent block on disk.  (because that logic runs concurrently with ingestion without a lock)
2) The labels don't validate. (if the set is empty or contains duplicate label names)
3) If the sample, for the respective series (based on all the labels) is out of order or has a different value for the last (highest) timestamp seen. (results in `storage.ErrOutOfOrderSample` and `storage.ErrDuplicateSampleForTimestamp` respectively)

`Commit()` may also refuse data that is out of order with respect to samples that were added via a different appender.

## Querying data

Use [`db.Querier()`](https://pkg.go.dev/github.com/prometheus/prometheus/tsdb#DB.Querier) to obtain a "querier".
The [golang docs](https://pkg.go.dev/github.com/prometheus/prometheus/storage#Querier) speak mostly for themselves.

Remember:

* A querier can only see data that was committed when it was created. This limits the lifetime of a querier.
* A querier should be closed when you're done with it.
* Use mint/maxt to avoid loading unneeded data.

